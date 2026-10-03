#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 RPG Maker MV 游戏，生成 ScenePlayer 插件需要的参数。

用法示例：
    # 输出 sceneList / missingAssets 两个参数字符串（可直接粘进 plugins.js）
    python3 tools/scan_game.py /path/to/game/www

    # 直接输出可粘进 plugins.js 的整条插件条目
    python3 tools/scan_game.py /path/to/game/www --emit entry

    # 人肉检查用：一行一个场景
    python3 tools/scan_game.py /path/to/game/www --emit list

    # 换匹配规则 / 排除 id / 指定显示名
    python3 tools/scan_game.py /path/to/game/www --pattern "cg|scene" --exclude 410,411
    python3 tools/scan_game.py /path/to/game/www --names names.json

依赖：仅 Python 3 标准库。
"""

import argparse
import glob
import json
import os
import re
import sys

import tagging

IMG_EXTS = ('.rpgmvp', '.png', '.jpg', '.jpeg', '.webp')
# 不算「内容」的指令：0=结束、108/408=注释
NOOP_CODES = (0, 108, 408)


def log(*args):
    print(*args, file=sys.stderr)


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def resolve_dirs(given):
    """返回 (数据目录, 图片目录)。允许传游戏根目录、www/、或 data/ 本身。"""
    cands = [given, os.path.join(given, 'www'), os.path.join(os.path.dirname(given), '')]
    for base in cands:
        data_dir = os.path.join(base, 'data')
        if os.path.isfile(os.path.join(data_dir, 'CommonEvents.json')):
            return data_dir, os.path.join(base, 'img', 'pictures')
    if os.path.isfile(os.path.join(given, 'CommonEvents.json')):
        base = os.path.dirname(given)
        return given, os.path.join(os.path.dirname(base), 'img', 'pictures')
    raise SystemExit(
        '找不到 data/CommonEvents.json。请把「含 data/ 和 img/pictures/ 的那层目录」'
        '（通常是 <游戏目录>/www）传给本脚本。')


def load_common_events(data_dir):
    """读取 data/CommonEvents.json，返回 {id: event}。"""
    path = os.path.join(data_dir, 'CommonEvents.json')
    if not os.path.isfile(path):
        raise SystemExit('找不到 %s，无法扫描场景。' % path)
    by_id = {}
    for event in json.load(open(path, encoding='utf-8')):
        if event:
            by_id[event['id']] = event
    return by_id


MOVIE_EXTS = ('.webm', '.mp4', '.m4v', '.ogg')


def movie_index(www):
    """返回 (影片名集合 或 None, 影片目录)。文件名去掉扩展名。"""
    dirs = [os.path.join(www, 'movies'), os.path.join(os.path.dirname(www), 'movies')]
    for d in dirs:
        if os.path.isdir(d):
            names = set()
            for fn in os.listdir(d):
                base, ext = os.path.splitext(fn)
                if ext.lower() in MOVIE_EXTS:
                    names.add(base)
            return names, d
    return None, dirs[0]


def picture_index(www):
    """返回 (图片名集合 或 None, 图片目录路径)。www = 含 img/ 的那层目录。"""
    pics_dir = os.path.join(www, 'img', 'pictures')
    if not os.path.isdir(pics_dir):
        return None, pics_dir
    return index_pictures(pics_dir), pics_dir


def index_pictures(pics_dir):
    """返回 {图片名: True}；目录不存在则返回 None。"""
    if not os.path.isdir(pics_dir):
        return None
    names = set()
    for fn in os.listdir(pics_dir):
        base, ext = os.path.splitext(fn)
        if ext.lower() in IMG_EXTS:
            names.add(base)
    return names


def has_content(event):
    return any(c.get('code') not in NOOP_CODES for c in event.get('list', []))


def pictures_of(event):
    return {str(c['parameters'][1]) for c in event.get('list', [])
            if c.get('code') == 231 and len(c.get('parameters') or []) > 1}


def has_dialogue(event):
    return any(c.get('code') == 401 and (c.get('parameters') or [''])[0].strip()
               for c in event.get('list', []))


def called_event_ids(by_id):
    """被别的事件用指令 117 调用过的公共事件 id（这些是子事件，不适合单独播）。"""
    return {c['parameters'][0] for e in by_id.values() for c in e.get('list', [])
            if c.get('code') == 117 and c.get('parameters')}


# 「看着像场景」但名字不含 scene 的事件：排除剧情枢纽 / 任务逻辑 / Anim 子事件
NOT_CG_NAME = re.compile(
    r'dialogue|quest|announce|grow|rent|travel|ledger|comment|briefing|niu|'
    r'disguise|intro$|^Anim|meeting|follow|build|clean|give|take|catch|'
    r'waiting|arrives|arrive|detected|knock|purifier|lord|showdown|cleared', re.I)

# 名字里的「场景感」关键词
CG_NAME = re.compile(
    r'sex|bed|bath|strip|mass|bj|blow|threesome|preg|naked|lingerie|tits|pussy|kiss|'
    r'mast|breed|dominat|createchild|swim|visit|peek|table|chair|well|forest|cemetery|'
    r'chapel|crypt|armory|bakery|cabin|lodge|tent|pool|garden|stage|hybrid|victim', re.I)


def map_key(map_id, event_id):
    """地图场景在 missingAssets / names 里的键。"""
    return 'm%d:%d' % (map_id, event_id)


def load_maps(data_dir):
    """读取 data/Map###.json，返回 [(mapId, displayName, {eventId: event})]。"""
    out = []
    for fn in sorted(glob.glob(os.path.join(data_dir, 'Map[0-9][0-9][0-9].json'))):
        map_id = int(os.path.basename(fn)[3:-5])
        try:
            data = json.load(open(fn, encoding='utf-8'))
        except (ValueError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        out.append((map_id, data.get('displayName') or ('Map%03d' % map_id), data.get('events') or []))
    return out


def event_commands(event):
    """地图事件的所有指令（跨所有事件页）。"""
    return [c for page in (event.get('pages') or []) for c in (page.get('list') or [])]


def scan_map_scenes(data_dir, names, min_pics=5, exclude_maps=None, by_id=None):
    """扫描地图事件里的场景。

    口径：含「显示图片」>= min_pics 张，且至少有一句对白。
    返回 [map_scene, ...]，每项 = [mapId, eventId, x, y, 显示名, 原始名]
    """
    exclude_maps = exclude_maps or set()
    names = names or {}
    out = []
    for map_id, display, events in load_maps(data_dir):
        if map_id in exclude_maps:
            continue
        for event in events:
            if not event:
                continue
            cmds = event_commands(event)
            pics = {str(c['parameters'][1]) for c in cmds
                    if c.get('code') == 231 and len(c.get('parameters') or []) > 1}
            if len(pics) < min_pics:
                continue
            if not any(c.get('code') == 401 and (c.get('parameters') or [''])[0].strip() for c in cmds):
                continue
            event_id = event['id']
            orig = 'Map%03d #%d %s' % (map_id, event_id, event.get('name') or '')
            label = names.get(map_key(map_id, event_id)) or ('%s · 事件%d' % (display, event_id))
            out.append([map_id, event_id, event['x'], event['y'], label, orig])
    out.sort(key=lambda r: (r[0], r[1]))
    return out


def map_event_trigger(data_dir, map_id, event_id):
    """地图事件第一页的触发方式（0确定/1玩家接触/2事件接触/3自动/4并行）。"""
    for mid, _, events in load_maps(data_dir):
        if mid != map_id:
            continue
        for event in events:
            if event and event['id'] == event_id:
                pages = event.get('pages') or []
                return pages[0].get('trigger') if pages else None
    return None


def build_tags(ce_scenes, map_scenes):
    """生成 {键: 标签}，键为公共事件 id 字符串或 "m<mapId>:<eventId>"。"""
    tags = {}
    for row in ce_scenes:
        tags[str(row[0])] = tagging.ce_tag(row[0])
    for row in map_scenes:
        tags[map_key(row[0], row[1])] = tagging.map_tag(map_key(row[0], row[1]))
    return tags


def closure_assets(by_id, event_id, seen=None):
    """事件自身 + 递归调用的公共事件里用到的 (图片名集合, 影片名集合)。"""
    if seen is None:
        seen = set()
    if event_id in seen:
        return set(), set()
    seen.add(event_id)
    event = by_id.get(event_id)
    if not event:
        return set(), set()
    pics, movies = set(), set()
    for cmd in event.get('list', []):
        params = cmd.get('parameters') or []
        if cmd.get('code') == 231 and len(params) > 1:
            pics.add(str(params[1]))
        elif cmd.get('code') == 261 and params:
            movies.add(str(params[0]))
        elif cmd.get('code') == 117 and params:
            p, m = closure_assets(by_id, params[0], seen)
            pics |= p
            movies |= m
    return pics, movies


def missing_of_closure(by_id, event_id, have_pics, have_movies):
    """返回该场景缺失的资产名列表；影片用 'movie:' 前缀标记。"""
    pics, movies = closure_assets(by_id, event_id)
    gone = []
    if have_pics is not None:
        gone += sorted(p for p in pics if p not in have_pics)
    if have_movies is not None:
        gone += sorted('movie:' + m for m in movies if m not in have_movies)
    return gone


def map_scene_assets(data_dir, by_id, scene):
    """地图场景用到的 (图片, 影片)：事件自身 + 它调用的公共事件。"""
    map_id, event_id = scene[0], scene[1]
    for mid, _, events in load_maps(data_dir):
        if mid != map_id:
            continue
        for event in events:
            if event and event['id'] == event_id:
                cmds = event_commands(event)
                pics = {str(c['parameters'][1]) for c in cmds
                        if c.get('code') == 231 and len(c.get('parameters') or []) > 1}
                movies = {str(c['parameters'][0]) for c in cmds
                          if c.get('code') == 261 and c.get('parameters')}
                for c in cmds:
                    if c.get('code') == 117 and c.get('parameters') and by_id:
                        p, m = closure_assets(by_id, c['parameters'][0])
                        pics |= p
                        movies |= m
                return pics, movies
    return set(), set()


def map_scene_pictures(data_dir, by_id, scene):
    """地图场景用到的全部图片：事件自身 + 它调用的公共事件（递归）。"""
    map_id, event_id = scene[0], scene[1]
    for mid, _, events in load_maps(data_dir):
        if mid != map_id:
            continue
        for event in events:
            if event and event['id'] == event_id:
                pics = {str(c['parameters'][1]) for c in event_commands(event)
                        if c.get('code') == 231 and len(c.get('parameters') or []) > 1}
                for c in event_commands(event):
                    if c.get('code') == 117 and c.get('parameters') and by_id:
                        pics |= closure_pictures(by_id, c['parameters'][0])
                return pics
    return set()


def select_scenes(by_id, pattern, exclude, names, mode='scene', min_pics=4):
    """按不同口径挑选场景。

    scene    : 事件名匹配 pattern（默认）
    auto     : pattern 命中，或「像顶层场景」的（有图 + 有对白 + 无人调用 + trigger=0，
               且图片数 >= min_pics 或名字带场景感关键词，并排除剧情枢纽 / Anim*）
    all-pics : 所有含「显示图片」且有实际指令的事件
    """
    rx = re.compile(pattern, re.I)
    called = called_event_ids(by_id)
    scenes = []
    for event_id in sorted(by_id):
        if event_id in exclude:
            continue
        event = by_id[event_id]
        if not has_content(event):
            continue
        name = event.get('name') or ''
        hit = bool(rx.search(name))
        if mode == 'all-pics':
            hit = bool(pictures_of(event))
        elif mode == 'auto' and not hit:
            pics = pictures_of(event)
            hit = (event.get('trigger') == 0 and event_id not in called
                   and bool(pics) and has_dialogue(event)
                   and not NOT_CG_NAME.search(name)
                   and (len(pics) >= min_pics or bool(CG_NAME.search(name))))
        if not hit:
            continue
        scenes.append([event_id, names.get(event_id) or name or ('#' + str(event_id)), name])
    return scenes


def closure_pictures(by_id, event_id, seen=None):
    """事件自身 + 递归调用的公共事件（指令 117）里用到的所有图片名。"""
    if seen is None:
        seen = set()
    if event_id in seen:
        return set()
    seen.add(event_id)
    event = by_id.get(event_id)
    if not event:
        return set()
    pics = set()
    for cmd in event.get('list', []):
        params = cmd.get('parameters') or []
        if cmd.get('code') == 231 and len(params) > 1:
            pics.add(str(params[1]))
        elif cmd.get('code') == 117 and params:
            pics |= closure_pictures(by_id, params[0], seen)
    return pics


def collect(data_dir, www, pattern='scene', exclude=(), names=None,
            mode='auto', min_pics=4, maps=False, map_min_pics=5, map_triggers=(0, 1, 2)):
    """一条流水线：扫公共事件 + 扫地图事件 + 缺素材 + 类型标签。

    返回 dict(scenes, map_scenes, missing, tags, have, pics_dir, by_id)。
    """
    names = names or {}
    by_id = load_common_events(data_dir)
    scenes = select_scenes(by_id, pattern, exclude, names, mode, min_pics)
    have, pics_dir = picture_index(www)
    have_movies, movies_dir = movie_index(www)
    missing = {}
    for event_id, _, _ in scenes:
        gone = missing_of_closure(by_id, event_id, have, have_movies)
        if gone:
            missing[str(event_id)] = gone
    map_scenes = []
    if maps:
        want = set(map_triggers)
        map_scenes = [r for r in scan_map_scenes(data_dir, names, map_min_pics, by_id=by_id)
                      if map_event_trigger(data_dir, r[0], r[1]) in want]
        for row in map_scenes:
            pics, movies = map_scene_assets(data_dir, by_id, row)
            gone = []
            if have is not None:
                gone += sorted(p for p in pics if p not in have)
            if have_movies is not None:
                gone += sorted('movie:' + m for m in movies if m not in have_movies)
            if gone:
                missing[map_key(row[0], row[1])] = gone
    return dict(by_id=by_id, scenes=scenes, map_scenes=map_scenes, missing=missing,
                tags=build_tags(scenes, map_scenes), have=have, pics_dir=pics_dir,
                have_movies=have_movies, movies_dir=movies_dir)


def main():
    ap = argparse.ArgumentParser(
        description='扫描 RPG Maker MV 游戏，生成 ScenePlayer 的 sceneList / missingAssets 参数。',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('game_dir', help='含 data/ 与 img/pictures/ 的目录（通常是 <游戏>/www）')
    ap.add_argument('--pattern', default='scene',
                    help='事件名匹配的正则，不区分大小写（默认 scene）')
    ap.add_argument('--mode', choices=['scene', 'auto', 'all-pics'], default='scene',
                    help='scene=只按事件名匹配(默认)；auto=再加上「像顶层场景」的；'
                         'all-pics=所有含「显示图片」的事件')
    ap.add_argument('--min-pics', type=int, default=4,
                    help='auto 模式下图片数达到多少张才算场景（默认 4）')
    ap.add_argument('--maps', action='store_true',
                    help='同时扫描地图事件里的场景（指令在 pages[].list，本插件会先传送再触发）')
    ap.add_argument('--map-min-pics', type=int, default=5,
                    help='地图事件图片数达到多少张才算场景（默认 5）')
    ap.add_argument('--map-triggers', default='0,1,2',
                    help='只收这些触发方式的地图事件（0确定/1玩家接触/2事件接触/3自动/4并行），默认 0,1,2')
    ap.add_argument('--exclude', default='',
                    help='要排除的事件 id，逗号分隔，如 410,411,487')
    ap.add_argument('--names', default=None,
                    help='JSON 文件 {"事件id": "显示名"}，用于给列表项加自定义名（可中文）')
    ap.add_argument('--emit', choices=['json', 'entry', 'list'], default='json',
                    help='json=参数字符串(默认) entry=plugins.js 整条 list=人读清单')
    ap.add_argument('--plugin-name', default='ScenePlayer', help='插件名（默认 ScenePlayer）')
    args = ap.parse_args()

    data_dir, pics_dir = resolve_dirs(args.game_dir)

    try:
        re.compile(args.pattern, re.I)
    except re.error as e:
        raise SystemExit('--pattern 不是合法正则: %s' % e)

    exclude = set()
    for part in args.exclude.split(','):
        part = part.strip()
        if part:
            exclude.add(int(part))

    names = {}
    if args.names:
        for k, v in load_json(args.names).items():
            # 键既可能是公共事件 id（"295"），也可能是地图场景（"m1:81"）
            if str(k).startswith('m'):
                names[str(k)] = str(v)
            else:
                names[int(k)] = str(v)

    res = collect(data_dir, os.path.dirname(os.path.dirname(pics_dir)), args.pattern,
                  exclude, names, args.mode, args.min_pics, args.maps,
                  args.map_min_pics, [int(x) for x in args.map_triggers.split(',') if x.strip()])
    scenes = res['scenes']
    map_scenes = res['map_scenes']
    missing = res['missing']
    tags = res['tags']
    by_id = res['by_id']
    have = res['have']
    if have is None:
        log('! 找不到图片目录 %s，跳过图片检测' % pics_dir)
    if res['have_movies'] is None:
        log('! 找不到影片目录 %s，跳过影片检测' % res['movies_dir'])

    scene_list = json.dumps(scenes, ensure_ascii=False, separators=(',', ':'))
    map_scene_list = json.dumps(map_scenes, ensure_ascii=False, separators=(',', ':'))
    missing_assets = json.dumps(missing, ensure_ascii=False, separators=(',', ':'))
    tag_json = json.dumps(tags, ensure_ascii=False, separators=(',', ':'))

    log('数据目录: %s' % data_dir)
    log('图片目录: %s%s' % (pics_dir, '' if have is not None else '（不存在）'))
    log('挑选口径: %s%s' % (args.mode, '' if args.mode != 'auto' else '（min-pics=%d）' % args.min_pics))
    log('候选场景: %d 个（公共事件）%s' % (len(scenes),
        '  + %d 个（地图事件）' % len(map_scenes) if map_scenes else ''))
    if tags:
        from collections import Counter
        log('类型标签: %s' % dict(Counter(tags.values())))
    if missing:
        n_pic = sum(1 for v in missing.values() for x in v if not x.startswith('movie:'))
        n_mov = sum(1 for v in missing.values() for x in v if x.startswith('movie:'))
        log('缺素材场景: %d 个（缺图 %d 张 + 缺影片 %d 个）' % (len(missing), n_pic, n_mov))
        for key, gone in list(missing.items()):
            if key.startswith('m'):
                mid, eid = key[1:].split(':')
                name = 'Map%03d #%s' % (int(mid), eid)
            else:
                name = by_id[int(key)].get('name')
            log('  %-12s %-38s 缺 %d 项  例: %s' % (key, name, len(gone), gone[0]))
    else:
        log('缺素材场景: 0 个')

    if args.emit == 'list':
        for event_id, display, orig in scenes:
            flag = '  ⚠缺素材' if str(event_id) in missing else ''
            print('%-6s [%-5s] %-32s %s%s' % (event_id, tags.get(str(event_id), '?'),
                                              display, orig, flag))
        for row in map_scenes:
            key = map_key(row[0], row[1])
            flag = '  ⚠缺素材' if key in missing else ''
            print('%-6s [%-5s] %-32s %s%s' % ('地图', tags.get(key, '?'), row[4], row[5], flag))
        return

    if args.emit == 'entry':
        entry = {
            'name': args.plugin_name,
            'status': True,
            'description': 'v2.0.0 场景速播器：F7 列表 / F8 下一个 / F9 自动连播 / F10 自动推进对话',
            'parameters': {
                'sceneList': scene_list,
                'openKey': '118',
                'nextKey': '119',
                'autoKey': '120',
                'msgKey': '121',
                'autoDelay': '60',
                'msgDelay': '45',
                'filterKey': '117',
                'missingAssets': missing_assets,
                'mapScenes': map_scene_list,
                'tags': tag_json,
            },
        }
        print(json.dumps(entry, ensure_ascii=False))
        return

    print(json.dumps({'sceneList': scene_list, 'mapScenes': map_scene_list,
                      'missingAssets': missing_assets, 'tags': tag_json},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
