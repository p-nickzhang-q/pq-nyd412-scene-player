#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正《农民的任务》NYD412 里 VirtualacgPC 的 unlockEvents：剔除缺素材的场景 id。

背景：作弊菜单「解锁公共事件」读的是 `VirtualacgPC -> parameters.unlockEvents`，
那个菜单不做素材检查，选到缺图场景会直接把游戏打成 `Loading Error`。
本脚本把这 15 个 id 从 unlockEvents 里删掉（162 -> 147）。

用法：
    # 先看看会改什么，不落盘
    python3 tools/fix-unlock-events.py "/path/to/农民的任务/www" --dry-run

    # 执行（会自动备份 plugins.js.bak-<时间戳>）
    python3 tools/fix-unlock-events.py "/path/to/农民的任务/www"

    # 装了可选内容包之后，把 162 个全加回来
    python3 tools/fix-unlock-events.py "/path/to/农民的任务/www" --restore

缺素材 id 默认取 ScenePlayer 参数里的 missingAssets；没装 ScenePlayer 时用 --drop 指定：
    python3 tools/fix-unlock-events.py "/path/to/game/www" \
        --drop 295,297,298,497,1250,1251,1254,1491,1498,1644,1823,1829,1833,1837,1838
"""

import argparse
import json
import os
import re
import shutil
import sys
import time

PLUGIN_JS = os.path.join('js', 'plugins.js')
UNLOCK_KEY = 'VirtualacgPC'
UNLOCK_PARAM = 'unlockEvents'
SCENE_PLAYER = 'ScenePlayer'


def log(*args):
    print(*args, file=sys.stderr)


def find_plugins_js(given):
    cands = [
        os.path.join(given, PLUGIN_JS),
        os.path.join(given, 'www', PLUGIN_JS),
        given if given.endswith('plugins.js') else None,
    ]
    for path in cands:
        if path and os.path.isfile(path):
            return path
    raise SystemExit('找不到 js/plugins.js。请把「含 js/ 的那层目录」（通常是 <游戏>/www）传给本脚本。')


def parse_entries(text):
    match = re.search(r'var \$plugins\s*=\s*(\[[\s\S]*\]);', text)
    if not match:
        raise SystemExit('plugins.js 里找不到 `var $plugins = [...]`，文件结构可能被改过。')
    return json.loads(match.group(1))


def entry_by_name(entries, name):
    for entry in entries:
        if entry.get('name') == name:
            return entry
    return None


def main():
    ap = argparse.ArgumentParser(description='剔除/恢复 unlockEvents 里缺素材的场景 id。')
    ap.add_argument('game_dir', help='含 js/plugins.js 的目录（通常是 <游戏>/www）')
    ap.add_argument('--dry-run', action='store_true', help='只报告，不写文件')
    ap.add_argument('--restore', action='store_true', help='反向操作：把 ScenePlayer 的 162 个 id 全写回去')
    ap.add_argument('--drop', default='', help='手工指定要剔除的 id，逗号分隔（默认取 ScenePlayer.missingAssets）')
    args = ap.parse_args()

    path = find_plugins_js(args.game_dir)
    text = open(path, encoding='utf-8').read()
    entries = parse_entries(text)

    unlock = entry_by_name(entries, UNLOCK_KEY)
    if unlock is None:
        raise SystemExit('plugins.js 里没有 %s 插件，无事可做。' % UNLOCK_KEY)
    current = json.loads(unlock['parameters'][UNLOCK_PARAM])

    player = entry_by_name(entries, SCENE_PLAYER)
    if player is not None:
        scenes = [row[0] for row in json.loads(player['parameters']['sceneList'])]
        missing = sorted(int(k) for k in json.loads(player['parameters']['missingAssets']))
    else:
        scenes, missing = [], []

    if args.drop:
        drop = sorted({int(x) for x in args.drop.split(',') if x.strip()})
    elif missing:
        drop = missing
    else:
        raise SystemExit('既没装 ScenePlayer（拿不到 missingAssets），也没给 --drop，无法判断要剔除哪些。')

    if args.restore:
        if not scenes:
            raise SystemExit('--restore 需要 ScenePlayer 的 sceneList 才能知道完整 id 集合。')
        target = sorted(scenes)
        action = '恢复'
    else:
        drop_set = set(drop)
        target = [i for i in current if i not in drop_set]
        action = '剔除'

    removed = [i for i in current if i not in set(target)]
    added = [i for i in target if i not in set(current)]

    log('plugins.js     : %s' % path)
    log('unlockEvents   : %d -> %d 个（%s）' % (len(current), len(target), action))
    if removed:
        log('移除的 id      : %s' % removed)
    if added:
        log('加回的 id      : %s' % added)
    if not removed and not added:
        log('已经是目标状态，无需改动。')
        return

    if args.dry_run:
        log('--dry-run：未写入文件。')
        return

    match = re.search(r'("unlockEvents":\s*")(\[[^"]*\])(\s*")', text)
    if not match:
        raise SystemExit('在 plugins.js 里定位不到 unlockEvents 的字面量，为安全起见已中止（未修改文件）。')

    backup = '%s.bak-%s' % (path, time.strftime('%Y%m%d-%H%M%S'))
    seq = 2
    while os.path.exists(backup):      # 同一秒内多次运行也不能互相覆盖备份
        backup = '%s.bak-%s-%d' % (path, time.strftime('%Y%m%d-%H%M%S'), seq)
        seq += 1
    shutil.copy2(path, backup)
    log('备份           : %s' % backup)

    new_text = text[:match.start(2)] + json.dumps(target, separators=(',', ':')) + text[match.end(2):]
    open(path, 'w', encoding='utf-8').write(new_text)

    # 回读校验：整体仍是合法 JSON，且 unlockEvents 符合预期
    check = parse_entries(new_text)
    got = json.loads(entry_by_name(check, UNLOCK_KEY)['parameters'][UNLOCK_PARAM])
    if got != target:
        raise SystemExit('写入后校验失败，请用备份还原: %s' % backup)
    log('校验           : 通过（%d 个 id，%d 个插件条目结构完好）' % (len(got), len(check)))


if __name__ == '__main__':
    main()
