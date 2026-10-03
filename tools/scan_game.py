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
import json
import os
import re
import sys

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


def main():
    ap = argparse.ArgumentParser(
        description='扫描 RPG Maker MV 游戏，生成 ScenePlayer 的 sceneList / missingAssets 参数。',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('game_dir', help='含 data/ 与 img/pictures/ 的目录（通常是 <游戏>/www）')
    ap.add_argument('--pattern', default='scene',
                    help='事件名匹配的正则，不区分大小写（默认 scene）')
    ap.add_argument('--exclude', default='',
                    help='要排除的事件 id，逗号分隔，如 410,411,487')
    ap.add_argument('--names', default=None,
                    help='JSON 文件 {"事件id": "显示名"}，用于给列表项加自定义名（可中文）')
    ap.add_argument('--emit', choices=['json', 'entry', 'list'], default='json',
                    help='json=参数字符串(默认) entry=plugins.js 整条 list=人读清单')
    ap.add_argument('--plugin-name', default='ScenePlayer', help='插件名（默认 ScenePlayer）')
    args = ap.parse_args()

    data_dir, pics_dir = resolve_dirs(args.game_dir)
    by_id = {}
    for event in load_json(os.path.join(data_dir, 'CommonEvents.json')):
        if event:
            by_id[event['id']] = event

    try:
        rx = re.compile(args.pattern, re.I)
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
            names[int(k)] = str(v)

    have = index_pictures(pics_dir)
    if have is None:
        log('! 找不到图片目录 %s，跳过缺素材检测' % pics_dir)

    scenes, missing = [], {}
    for event_id in sorted(by_id):
        event = by_id[event_id]
        if event_id in exclude:
            continue
        if not rx.search(event.get('name') or ''):
            continue
        if not has_content(event):
            continue
        display = names.get(event_id) or (event.get('name') or ('#' + str(event_id)))
        scenes.append([event_id, display, event.get('name') or ''])
        if have is not None:
            gone = sorted(p for p in closure_pictures(by_id, event_id) if p not in have)
            if gone:
                missing[str(event_id)] = gone

    scene_list = json.dumps(scenes, ensure_ascii=False, separators=(',', ':'))
    missing_assets = json.dumps(missing, ensure_ascii=False, separators=(',', ':'))

    log('数据目录: %s' % data_dir)
    log('图片目录: %s%s' % (pics_dir, '' if have is not None else '（不存在）'))
    log('候选场景: %d 个' % len(scenes))
    if missing:
        log('缺素材场景: %d 个（共 %d 张图）' % (len(missing), sum(len(v) for v in missing.values())))
        for event_id, gone in list(missing.items()):
            name = by_id[int(event_id)].get('name')
            log('  #%-5s %-38s 缺 %d 张  例: %s' % (event_id, name, len(gone), gone[0]))
    elif have is not None:
        log('缺素材场景: 0 个')

    if args.emit == 'list':
        for event_id, display, orig in scenes:
            flag = '  ⚠缺素材' if str(event_id) in missing else ''
            print('%-6s %-34s %s%s' % (event_id, display, orig, flag))
        return

    if args.emit == 'entry':
        entry = {
            'name': args.plugin_name,
            'status': True,
            'description': 'v1.1.0 场景速播器：F7 列表 / F8 下一个 / F9 自动连播 / F10 自动推进对话',
            'parameters': {
                'sceneList': scene_list,
                'openKey': '118',
                'nextKey': '119',
                'autoKey': '120',
                'msgKey': '121',
                'autoDelay': '60',
                'msgDelay': '45',
                'missingAssets': missing_assets,
            },
        }
        print(json.dumps(entry, ensure_ascii=False))
        return

    print(json.dumps({'sceneList': scene_list, 'missingAssets': missing_assets},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
