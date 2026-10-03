#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""《农民的任务》NYD412 场景速播器 —— 一键安装/更新脚本。

一条命令搞定：
  1. 环境自检（确认是 RPG Maker MV、定位 www/ 与 js/plugins.js）
  2. 把 ScenePlayer.js 复制/更新到 js/plugins/（旧文件自动备份）
  3. 扫描 data/CommonEvents.json 生成 sceneList（含中文名）
  4. 扫描 img/pictures 生成 missingAssets（沿指令 117 递归，能发现子事件缺图）
  5. 写入/更新 js/plugins.js 里的 ScenePlayer 条目（只动这一条，其余原样保留）
  6. 修正 VirtualacgPC 的 unlockEvents，剔除缺素材的场景 id（避免作弊菜单选到就 Loading Error）

用法：
    # 先看会改什么（不写任何文件）
    python3 tools/setup.py "/path/to/农民的任务"

    # 正式执行
    python3 tools/setup.py "/path/to/农民的任务" --yes

    # 只更新参数，不碰 unlockEvents
    python3 tools/setup.py "/path/to/农民的任务" --no-unlock --yes

    # 以后装了可选内容包（Spicy Mod），把 unlockEvents 恢复成全部场景
    python3 tools/setup.py "/path/to/农民的任务" --restore --yes

参数默认值都按本作调好了，正常情况下**不需要带任何选项**。
依赖：仅 Python 3 标准库。
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time

IMG_EXTS = ('.rpgmvp', '.png', '.jpg', '.jpeg', '.webp')
PLUGIN_NAME = 'ScenePlayer'
UNLOCK_PLUGIN = 'VirtualacgPC'
UNLOCK_PARAM = 'unlockEvents'
DEFAULT_PATTERN = 'scene'
# 本作真正非 CG 的 5 个：SceneIntro/SceneExtro（系统过场）、AnimPixieScene1-Cam1/2/3（动画子事件）
DEFAULT_EXCLUDE = '410,411,1894,1895,1896'
DEFAULT_MODE = 'auto'
DEFAULT_MIN_PICS = 4
DEFAULT_KEYS = {'openKey': '118', 'nextKey': '119', 'autoKey': '120',
                'msgKey': '121', 'autoDelay': '60', 'msgDelay': '45'}
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# 复用 scan_game 的扫描/挑选逻辑，避免两个工具口径不一致
sys.path.insert(0, HERE)
import scan_game  # noqa: E402


def log(*args):
    print(*args, file=sys.stderr)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def backup(path):
    """备份到 <path>.bak-<时间戳>，同秒多次运行也不会互相覆盖。"""
    stamp = time.strftime('%Y%m%d-%H%M%S')
    dest = '%s.bak-%s' % (path, stamp)
    seq = 2
    while os.path.exists(dest):
        dest = '%s.bak-%s-%d' % (path, stamp, seq)
        seq += 1
    shutil.copy2(path, dest)
    return dest


# ---------------------------------------------------------------------------
# 定位游戏
# ---------------------------------------------------------------------------

def resolve_game(given):
    """返回 (www目录, data目录, plugins.js 路径)。"""
    cands = [given, os.path.join(given, 'www')]
    for base in cands:
        pj = os.path.join(base, 'js', 'plugins.js')
        if os.path.isfile(pj):
            return base, os.path.join(base, 'data'), pj
    if os.path.basename(given) == 'plugins.js' and os.path.isfile(given):
        base = os.path.dirname(os.path.dirname(given))
        return base, os.path.join(base, 'data'), given
    raise SystemExit(
        '定位不到 js/plugins.js。请把「含 js/ 的那层目录」（通常是 <游戏根目录> 或 <游戏根目录>/www）传进来。')


def check_engine(www):
    core = os.path.join(www, 'js', 'rpg_core.js')
    if not os.path.isfile(core):
        raise SystemExit('找不到 js/rpg_core.js，这似乎不是 RPG Maker 游戏目录。')
    text = open(core, encoding='utf-8', errors='replace').read()
    match = re.search(r"RPGMAKER_NAME\s*=\s*'([^']+)'", text)
    name = match.group(1) if match else '?'
    if name != 'MV':
        raise SystemExit('检测到引擎是 %s，本插件只支持 MV（本作虽然自带的插件标了 @target MZ，'
                         '但实际引擎是 MV）。' % name)
    return name


# ---------------------------------------------------------------------------
# 扫描场景 / 缺素材
# ---------------------------------------------------------------------------

def locate_array(text):
    match = re.search(r'var\s+\$plugins\s*=\s*\[', text)
    if not match:
        raise SystemExit('plugins.js 里找不到 `var $plugins = [...]`，文件结构可能被改过。')
    return match.end()


def iter_entries(text):
    """返回 ([(obj, start, end), ...], 数组右括号位置)。用 raw_decode 精确定位每个条目。"""
    decoder = json.JSONDecoder()
    i = locate_array(text)
    entries = []
    while True:
        while i < len(text) and text[i] in ' \t\r\n,':
            i += 1
        if i >= len(text):
            raise SystemExit('plugins.js 的 $plugins 数组没有正常闭合（缺 `]`）。')
        if text[i] == ']':
            return entries, i
        obj, end = decoder.raw_decode(text, i)
        entries.append((obj, i, end))
        i = end


def find_entry(entries, name):
    for obj, start, end in entries:
        if obj.get('name') == name:
            return obj, start, end
    return None, None, None


def build_entry(scenes, missing, existing_params=None):
    params = dict(DEFAULT_KEYS)
    if existing_params:
        params.update({k: v for k, v in existing_params.items()
                       if k not in ('sceneList', 'missingAssets')})
    params['sceneList'] = json.dumps(scenes, ensure_ascii=False, separators=(',', ':'))
    params['missingAssets'] = json.dumps(missing, ensure_ascii=False, separators=(',', ':'))
    ordered = {'sceneList': params.pop('sceneList'),
               'openKey': params.pop('openKey', '118'),
               'nextKey': params.pop('nextKey', '119'),
               'autoKey': params.pop('autoKey', '120'),
               'msgKey': params.pop('msgKey', '121'),
               'autoDelay': params.pop('autoDelay', '60'),
               'msgDelay': params.pop('msgDelay', '45'),
               'missingAssets': params.pop('missingAssets')}
    ordered.update(params)          # 保留用户自己加的其它键
    return {'name': PLUGIN_NAME, 'status': True,
            'description': 'v1.2.0 场景速播器：F7 场景列表 / F8 下一个 / F9 自动连播 / F10 自动推进对话',
            'parameters': ordered}


def apply_entry(text, entries, array_end, entry):
    """写入/更新 ScenePlayer 条目，返回新文本。"""
    _, start, end = find_entry(entries, PLUGIN_NAME)
    new_json = json.dumps(entry, ensure_ascii=False)
    if start is not None:
        return text[:start] + new_json + text[end:]
    head = text[:array_end].rstrip()
    comma = '' if head.endswith('[') else ','
    return head + comma + '\n  ' + new_json + '\n' + text[array_end:]


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description='《农民的任务》NYD412 场景速播器一键安装/更新。')
    ap.add_argument('game_dir', help='游戏根目录，或 <根目录>/www，或 js/plugins.js 的路径')
    ap.add_argument('--dry-run', action='store_true', help='只报告，不写任何文件')
    ap.add_argument('--yes', '-y', action='store_true', help='不询问，直接执行')
    ap.add_argument('--restore', action='store_true',
                    help='把 unlockEvents 恢复成全部场景 id（装了可选内容包后用）')
    ap.add_argument('--rebuild-unlock', action='store_true',
                    help='用扫描结果重建 unlockEvents = 场景 id − 缺素材 id（现有列表不可信时用，例如本作原始的 [2041]）')
    ap.add_argument('--no-unlock', action='store_true', help='不改 unlockEvents')
    ap.add_argument('--no-install', action='store_true', help='不复制/更新 ScenePlayer.js')
    ap.add_argument('--pattern', default=DEFAULT_PATTERN, help='场景匹配正则（默认 scene）')
    ap.add_argument('--mode', choices=['scene', 'auto', 'all-pics'], default=DEFAULT_MODE,
                    help='scene=只按事件名匹配；auto=再加上「像顶层场景」的（默认，本作得到 306 个）；'
                         'all-pics=所有含「显示图片」的事件')
    ap.add_argument('--min-pics', type=int, default=DEFAULT_MIN_PICS,
                    help='auto 模式下图片数达到多少张才算场景（默认 4）')
    ap.add_argument('--exclude', default=DEFAULT_EXCLUDE, help='排除的事件 id，逗号分隔')
    ap.add_argument('--names', default=os.path.join(REPO, 'params', 'names.zh.json'),
                    help='中文名映射 JSON（默认用仓库里的 params/names.zh.json）')
    args = ap.parse_args()

    # --- 1. 定位与自检 ---
    www, data_dir, plugins_path = resolve_game(args.game_dir)
    engine = check_engine(www)
    log('引擎           : RPG Maker %s' % engine)
    log('游戏目录       : %s' % www)
    log('plugins.js     : %s' % plugins_path)

    exclude = {int(x) for x in args.exclude.split(',') if x.strip()}
    names = {}
    if args.names and os.path.isfile(args.names):
        names = {int(k): str(v) for k, v in json.load(open(args.names, encoding='utf-8')).items()}
        log('中文名映射     : %s（%d 条）' % (args.names, len(names)))
    else:
        log('中文名映射     : 未使用（列表将显示原始事件名）')

    # --- 2. 扫描 ---
    by_id = scan_game.load_common_events(data_dir)
    scenes = scan_game.select_scenes(by_id, args.pattern, exclude, names,
                                 args.mode, args.min_pics)
    have, pics_dir = scan_game.picture_index(www)
    missing = {}
    if have is None:
        log('缺素材检测     : 跳过（找不到 %s）' % pics_dir)
    else:
        for event_id, _, _ in scenes:
            gone = sorted(p for p in scan_game.closure_pictures(by_id, event_id) if p not in have)
            if gone:
                missing[str(event_id)] = gone
        log('图片素材       : %s（%d 个文件）' % (pics_dir, len(have)))
    log('场景           : %d 个（口径 %s%s，匹配 /%s/i，排除 %s）'
        % (len(scenes), args.mode,
           '' if args.mode != 'auto' else ' min-pics=%d' % args.min_pics,
           args.pattern, sorted(exclude) or '无'))
    log('缺素材场景     : %d 个（共 %d 张图）'
        % (len(missing), sum(len(v) for v in missing.values())))
    for event_id, gone in missing.items():
        log('   #%-5s %-34s 缺 %d 张' % (event_id, by_id[int(event_id)].get('name'), len(gone)))
    if not scenes:
        raise SystemExit('一个场景都没扫到，请检查 --pattern。')

    # --- 3. 规划文件改动 ---
    src_plugin = os.path.join(REPO, PLUGIN_NAME + '.js')
    dst_plugin = os.path.join(www, 'js', 'plugins', PLUGIN_NAME + '.js')
    plugin_action = None
    if args.no_install:
        plugin_action = 'skip'
    elif not os.path.isfile(src_plugin):
        raise SystemExit('仓库里找不到 %s，无法安装。' % src_plugin)
    elif not os.path.isfile(dst_plugin):
        plugin_action = 'install'
    elif sha256(src_plugin) != sha256(dst_plugin):
        plugin_action = 'update'
    else:
        plugin_action = 'same'

    text = open(plugins_path, encoding='utf-8').read()
    entries, array_end = iter_entries(text)
    existing, _, _ = find_entry(entries, PLUGIN_NAME)
    entry = build_entry(scenes, missing, existing['parameters'] if existing else None)
    entry_action = 'update' if existing else 'add'
    # 用语义比较判断是否需要写入：避免因空白/键序/description 措辞差异而反复重写
    entry_changed = (existing is None) or (existing != entry)
    # 语义一致就不动它的文本，只做必要的其它改动
    new_text = apply_entry(text, entries, array_end, entry) if entry_changed else text

    unlock_before = unlock_after = None
    unlock_bogus = []
    unlock_entry, ustart, uend = find_entry(entries, UNLOCK_PLUGIN)
    if unlock_entry is not None and not args.no_unlock:
        unlock_before = json.loads(unlock_entry['parameters'][UNLOCK_PARAM])
        scene_ids = {row[0] for row in scenes}
        unlock_bogus = [i for i in unlock_before if i not in by_id]
        if args.restore:
            unlock_after = sorted(scene_ids)
        elif args.rebuild_unlock:
            drop = {int(k) for k in missing}
            unlock_after = sorted(scene_ids - drop)
        else:
            drop = {int(k) for k in missing}
            unlock_after = [i for i in unlock_before if i not in drop]

    log('')
    log('计划改动：')
    log('  %-14s %s' % ('ScenePlayer.js', {
        'install': '安装到 js/plugins/（新文件）',
        'update': '更新（内容与仓库不同，旧文件会备份）',
        'same': '已是最新，跳过',
        'skip': '按 --no-install 跳过'}[plugin_action]))
    log('  %-14s %s 条目（%d 个场景 / %d 个缺素材场景）%s'
        % ('plugins.js', '写入' if entry_action == 'add' else '更新', len(scenes), len(missing),
           '' if entry_changed else '（内容已一致，跳过）'))
    if unlock_after is not None:
        log('  %-14s %d -> %d 个 id%s'
            % (UNLOCK_PLUGIN, len(unlock_before), len(unlock_after),
               '（--restore 恢复全部）' if args.restore else
               '（--rebuild-unlock 重建）' if args.rebuild_unlock else '（剔除缺素材场景）'))
        if unlock_bogus:
            log('  ⚠ 注意：现有 unlockEvents 里有 %d 个 id 在 CommonEvents.json 中不存在：%s'
                % (len(unlock_bogus), unlock_bogus))
            log('    （本作原始配置是 [2041]，而公共事件只到 2040，会导致菜单报「没有找到可解锁的公共事件」）')
            if not (args.rebuild_unlock or args.restore):
                log('    建议改用 --rebuild-unlock 重建。')
    elif unlock_entry is not None:
        log('  %-14s 按 --no-unlock 跳过' % UNLOCK_PLUGIN)
    else:
        log('  %-14s 游戏里没装这个插件，跳过' % UNLOCK_PLUGIN)

    changed = (plugin_action in ('install', 'update') or entry_changed
               or (unlock_after is not None and unlock_after != unlock_before))
    if not changed:
        log('')
        log('已是最新状态，无需改动。')
        return
    if args.dry_run:
        log('')
        log('--dry-run：未写入任何文件。')
        return

    # --- 4. 确认 ---
    if not args.yes:
        if not sys.stdin.isatty():
            raise SystemExit('需要确认但当前不是交互终端，请加 --yes 再执行（或先用 --dry-run 预览）。')
        answer = input('确认执行以上改动？[y/N] ').strip().lower()
        if answer not in ('y', 'yes'):
            raise SystemExit('已取消，未改动任何文件。')

    # --- 5. 落盘 ---
    if plugin_action in ('install', 'update'):
        if plugin_action == 'update':
            log('备份           : %s' % backup(dst_plugin))
        os.makedirs(os.path.dirname(dst_plugin), exist_ok=True)
        shutil.copy2(src_plugin, dst_plugin)
        log('已写入         : %s' % dst_plugin)

    # unlockEvents 单独处理：精准替换它自己的字面量，避免影响刚写入的条目
    final_text = new_text
    if unlock_after is not None and unlock_after != unlock_before:
        entries2, _ = iter_entries(new_text)
        _, start2, end2 = find_entry(entries2, UNLOCK_PLUGIN)
        pattern = re.compile(r'("' + UNLOCK_PARAM + r'":\s*")(\[[^"]*\])(\s*")')
        chunk = new_text[start2:end2]
        replaced, count = pattern.subn(
            lambda m: m.group(1) + json.dumps(unlock_after, separators=(',', ':')) + m.group(3), chunk)
        if count != 1:
            raise SystemExit('定位 unlockEvents 字面量失败（命中 %d 次），已中止，未写入 plugins.js。' % count)
        final_text = new_text[:start2] + replaced + new_text[end2:]

    log('备份           : %s' % backup(plugins_path))
    open(plugins_path, 'w', encoding='utf-8').write(final_text)

    # --- 6. 回读校验 ---
    check = open(plugins_path, encoding='utf-8').read()
    entries3, _ = iter_entries(check)
    got, _, _ = find_entry(entries3, PLUGIN_NAME)
    if got is None:
        raise SystemExit('写入后校验失败：找不到 ScenePlayer 条目。')
    got_scenes = json.loads(got['parameters']['sceneList'])
    got_missing = json.loads(got['parameters']['missingAssets'])
    if len(got_scenes) != len(scenes) or got_missing != missing:
        raise SystemExit('写入后校验失败：场景/缺素材数量不符。')
    if unlock_after is not None:
        got_unlock, _, _ = find_entry(entries3, UNLOCK_PLUGIN)
        if json.loads(got_unlock['parameters'][UNLOCK_PARAM]) != unlock_after:
            raise SystemExit('写入后校验失败：unlockEvents 不符。')
    log('校验           : 通过（%d 个插件条目结构完好）' % len(entries3))

    log('')
    log('完成。重启游戏（或按 F5）后生效：')
    log('  F7 场景列表    F8 下一个    F9 自动连播    F10 自动推进对话')
    log('  提示：自动连播会改开关/变量，建议先存一个独立存档。')


if __name__ == '__main__':
    main()
