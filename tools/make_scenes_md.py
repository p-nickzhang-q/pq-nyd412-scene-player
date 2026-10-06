#!/usr/bin/env python3
"""
重新生成 SCENES.md（场景对照表）。

从游戏里读插件参数 + 事件数据，逐条列出：类型 / id / 中文名 / 原始名 / 指令数 /
首句或首图 / 缺素材 / 是否在 unlockEvents / 是否子场景（被别的场景调用）。

用法：
    python3 tools/make_scenes_md.py "/path/to/游戏目录" > SCENES.md
    python3 tools/make_scenes_md.py "/path/to/游戏目录" --check   # 只报告与现有文件的差异
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nesting  # noqa: E402

TAG_LABEL = {'h': 'H', 'story': '剧情', 'misc': '杂项'}


def load_params(www):
    text = open(os.path.join(www, 'js', 'plugins.js'), encoding='utf-8').read()
    entries = json.loads(re.search(r'var\s+\$plugins\s*=\s*(\[[\s\S]*?\]);', text).group(1))
    by_name = {e.get('name'): e for e in entries}
    sp = by_name.get('ScenePlayer')
    if not sp:
        raise SystemExit('plugins.js 里没有 ScenePlayer 条目')
    return by_name, sp.get('parameters', {})


def first_line(cmd_list):
    r"""
    第一行对白正文(401)与首张图片(231)里先出现的那个。
    """
    # MV 的对话框是「101 说话人名（可为空）+ 401 正文行」。
    # 取「第一行 401 正文」与「首张图片 231」中先出现的那个 —— 开场就是图的场景
    # 显示图名，先出字的场景显示首句。
    for c in cmd_list:
        p = c.get('parameters') or []
        if c.get('code') == 401 and p and str(p[0]).strip():
            return str(p[0])
        if c.get('code') == 231 and len(p) > 1:
            return '[图 %s]' % p[1]
    return ''


def cell(text):
    """表格里不能出现裸 |，换行也要压平。"""
    return str(text).replace('|', '\\|').replace('\n', ' ')


def main():
    ap = argparse.ArgumentParser(description='重新生成 SCENES.md')
    ap.add_argument('game_dir')
    ap.add_argument('--check', action='store_true', help='与现有 SCENES.md 比较，不输出全文')
    args = ap.parse_args()

    www = nesting.find_www(args.game_dir)
    by_name, params = load_params(www)
    scenes = json.loads(params.get('sceneList') or '[]')
    map_scenes = json.loads(params.get('mapScenes') or '[]')
    tags = json.loads(params.get('tags') or '{}')
    missing = json.loads(params.get('missingAssets') or '{}')
    subs, info = nesting.analyze(www, scenes, map_scenes)

    ce = json.load(open(os.path.join(www, 'data', 'CommonEvents.json'), encoding='utf-8'))
    by_id = {e['id']: e for e in ce if e}

    # 作弊菜单的解锁列表存在 VirtualacgPC 插件里（不是独立插件）
    unlock = set()
    try:
        unlock = set(json.loads((by_name.get('VirtualacgPC') or {}).get('parameters', {})
                                .get('unlockEvents', '[]')))
    except (ValueError, TypeError):
        unlock = set()

    def missing_cell(key):
        gone = missing.get(key)
        if not gone:
            return '✅'
        n_mov = sum(1 for x in gone if x.startswith('movie:'))
        return '⚠ 缺 %d 项%s' % (len(gone), '（含影片 %d）' % n_mov if n_mov else '')

    def sub_cell(key):
        callers = subs.get(str(key))
        if not callers:
            return '—'
        names = []
        for c in callers[:2]:
            names.append(str(c) if str(c).startswith('m') else '#' + str(c))
        return '⊂ 被 %s 调用%s' % ('、'.join(names), ' 等 %d 处' % len(callers) if len(callers) > 2 else '')

    rows = []
    for i, s in enumerate(scenes):
        sid, name = s[0], s[1]
        e = by_id.get(sid) or {}
        lst = e.get('list', [])
        rows.append([str(i + 1), TAG_LABEL.get(tags.get(str(sid)), '?'), str(sid), cell(name),
                     cell(s[2] if len(s) > 2 else ''), str(len(lst)), cell(first_line(lst)),
                     missing_cell(str(sid)), '✅' if sid in unlock else '❌', sub_cell(sid)])
    for j, m in enumerate(map_scenes):
        key = 'm%d:%d' % (m[0], m[1])
        lst = nesting.map_event_list(www, m[0], m[1]) or []
        rows.append([str(len(scenes) + j + 1), TAG_LABEL.get(tags.get(key), '?'),
                     '🗺 Map%d#%d' % (m[0], m[1]), cell(m[4]), cell(m[5]),
                     '-', '(%d,%d)' % (m[2], m[3]), missing_cell(key), '—', sub_cell(key)])

    n_missing = len(missing)
    n_mov_scenes = sum(1 for v in missing.values() if any(x.startswith('movie:') for x in v))
    n_hidden = len(subs)

    out = []
    out.append('# 场景清单（%d 个：公共事件 %d + 地图事件 %d）\n' % (len(rows), len(scenes), len(map_scenes)))
    out.append('挑选口径：`tools/scan_game.py --mode auto --maps`'
               '（公共事件：名字含 Scene 或「像顶层场景」；地图事件：图片≥5 张+有对白+触发方式 0/1/2）\n')
    out.append('类型标签由 `tools/tagging.py` 的显式表给出'
               '（本作绝大多数场景含性内容，所以 H 是默认，剧情/杂项逐条人工确认）。\n')
    out.append('**缺素材 = 图片(231) 或影片(261) 文件不存在**。'
               '缺失影片会让 MV 反复重试加载（每个约 4.5 秒）把游戏卡住，因此也会被标 ⚠ 并跳过。\n')
    out.append('**子场景 = 被别的场景通过「调用公共事件」播到的场景**（由 `tools/nesting.py` 检测）。'
               '这类场景默认不在列表里显示，否则连播时会看到「大场景播一遍、里面的小场景又单独播一遍」。'
               '游戏内按 **F4** 可临时显示。\n')
    out.append('共 %d 个场景：**%d 个缺素材**（含影片缺失 %d 个）、**%d 个子场景默认隐藏**，'
               '列表默认显示 %d 项。\n' % (len(rows), n_missing, n_mov_scenes, n_hidden, len(rows) - n_hidden))
    if info['protected']:
        for keep, comp in info['protected']:
            out.append('> 环保护：%s 互相调用且没有环外入口，保留 #%d 可见，隐藏 %s。\n'
                       % ('、'.join('#%d' % x for x in comp), keep,
                          '、'.join('#%d' % x for x in comp if x != keep)))
    out.append('')
    out.append('| # | 类型 | id | 中文名 | 原始名 | 指令数 | 首句/首图 | 缺素材 | 在 unlockEvents | 子场景 |')
    out.append('|---|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        out.append('| ' + ' | '.join(r) + ' |')
    out.append('')
    text = '\n'.join(out)

    if args.check:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SCENES.md')
        old = open(path, encoding='utf-8').read() if os.path.isfile(path) else ''
        if old == text:
            print('SCENES.md 已是最新')
            return
        import difflib
        diff = list(difflib.unified_diff(old.splitlines(), text.splitlines(),
                                         'SCENES.md(旧)', 'SCENES.md(新)', lineterm='', n=0))
        print('SCENES.md 需要更新（%d 行差异）：' % len(diff))
        for line in diff[:40]:
            print('  ' + line)
        return
    sys.stdout.write(text)


if __name__ == '__main__':
    main()
