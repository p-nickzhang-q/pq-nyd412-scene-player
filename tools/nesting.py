#!/usr/bin/env python3
"""
检测「嵌套场景」：被其他场景通过指令 117（调用公共事件）播到的场景。

用途：某个场景内部把另一个场景也播了，而那个被调用的场景又单独占列表一项，
连播/浏览时就会看到重复内容。本工具算出「应当隐藏的子场景」清单，写进插件参数
subScenes，插件默认把它们从列表里排除（F4 可临时显示）。

规则
----
1. 被任何**列表内场景**（公共事件场景，或地图事件场景）调用过的公共事件场景
   → 隐藏（它就是"包含在别的场景里"的那个）。
2. 环的保护：互相调用（A→B→A）且**没有任何环外调用者**的一组，全部隐藏会让它们
   彻底没有入口，所以保留其中 id 最小的一个可见（标记为环入口）。

调用关系是递归/多层的（A 调 B，B 调 C），但规则 1 天然覆盖：C 被 B 调用 → 隐藏，
不论 B 自己是否也隐藏。

用法
----
    python3 tools/nesting.py "/path/to/游戏目录"            # 报告
    python3 tools/nesting.py "/path/to/游戏目录" --json      # 只输出参数 JSON
"""
import argparse
import collections
import json
import os
import re
import sys


def load_plugins(path):
    text = open(path, encoding='utf-8').read()
    m = re.search(r'var\s+\$plugins\s*=\s*(\[[\s\S]*?\]);', text)
    if not m:
        raise SystemExit('在 plugins.js 里找不到 var $plugins = [...]')
    return json.loads(m.group(1)), text


def find_www(game_dir):
    for cand in (game_dir, os.path.join(game_dir, 'www')):
        if os.path.isfile(os.path.join(cand, 'data', 'CommonEvents.json')):
            return cand
    raise SystemExit('找不到 %s/data/CommonEvents.json' % game_dir)


def called_ids(cmd_list, listed):
    """从指令表里取出调用的公共事件 id（只保留在列表内的）。"""
    out = []
    for c in cmd_list:
        if c.get('code') == 117:
            p = c.get('parameters') or []
            if p and p[0] in listed:
                out.append(p[0])
    return out


def map_event_list(www, map_id, event_id):
    path = os.path.join(www, 'data', 'Map%03d.json' % map_id)
    try:
        data = json.load(open(path, encoding='utf-8'))
    except (IOError, ValueError):
        return None
    for ev in data.get('events', []):
        if ev and ev.get('id') == event_id:
            return [c for pg in ev.get('pages', []) for c in pg.get('list', [])]
    return None


def find_cycles(edges):
    """找出互相调用的环（强连通分量，大小 > 1）。"""
    index = {}
    low = {}
    on = {}
    stack = []
    comps = []
    counter = [0]

    def strong(u):
        index[u] = low[u] = counter[0]
        counter[0] += 1
        stack.append(u)
        on[u] = True
        for v in edges.get(u, []):
            if v not in index:
                strong(v)
                low[u] = min(low[u], low[v])
            elif on.get(v):
                low[u] = min(low[u], index[v])
        if low[u] == index[u]:
            comp = []
            while True:
                w = stack.pop()
                on[w] = False
                comp.append(w)
                if w == u:
                    break
            comps.append(sorted(comp))

    for u in list(edges):
        if u not in index:
            strong(u)
    return [c for c in comps if len(c) > 1]


def analyze(www, scenes, map_scenes):
    """返回 (subs, info)：subs = {被隐藏场景键: [调用者键, ...]}"""
    ce = json.load(open(os.path.join(www, 'data', 'CommonEvents.json'), encoding='utf-8'))
    by_id = {e['id']: e for e in ce if e}
    listed = {s[0] for s in scenes}

    edges = {}          # 公共事件场景 -> 它调用的场景 id
    callers = collections.defaultdict(list)
    for s in scenes:
        e = by_id.get(s[0])
        if not e:
            continue
        targets = sorted(set(called_ids(e.get('list', []), listed)))
        edges[s[0]] = targets
        for t in targets:
            callers[t].append(s[0])

    for m in map_scenes:
        lst = map_event_list(www, m[0], m[1])
        if lst is None:
            continue
        key = 'm%d:%d' % (m[0], m[1])
        for t in sorted(set(called_ids(lst, listed))):
            callers[t].append(key)

    hidden = set(t for t in callers if t in listed)

    # 环保护：环内成员如果只被环内调用，保留 id 最小的那个
    protected = []
    for comp in find_cycles(edges):
        members = set(comp)
        outside = [c for x in comp for c in callers.get(x, []) if c not in members]
        if not outside:
            keep = comp[0]
            hidden.discard(keep)
            protected.append((keep, comp))

    subs = {}
    for t in sorted(hidden):
        subs[str(t)] = sorted(callers[t], key=lambda c: (isinstance(c, str), c))
    info = {
        'listed': len(listed),
        'hidden': len(hidden),
        'protected': protected,
        'edges': edges,
        'callers': dict(callers),
    }
    return subs, info


def main():
    ap = argparse.ArgumentParser(description='检测嵌套场景，生成插件参数 subScenes。')
    ap.add_argument('game_dir', help='游戏根目录或 www 目录')
    ap.add_argument('--json', action='store_true', help='只输出 subScenes 的 JSON')
    args = ap.parse_args()

    www = find_www(args.game_dir)
    entries, _ = load_plugins(os.path.join(www, 'js', 'plugins.js'))
    sp = [e for e in entries if e.get('name') == 'ScenePlayer']
    if not sp:
        raise SystemExit('plugins.js 里没有 ScenePlayer 条目')
    params = sp[0].get('parameters', {})
    scenes = json.loads(params.get('sceneList') or '[]')
    map_scenes = json.loads(params.get('mapScenes') or '[]')
    names = {str(s[0]): s[1] for s in scenes}
    mnames = {'m%d:%d' % (m[0], m[1]): m[4] for m in map_scenes}

    subs, info = analyze(www, scenes, map_scenes)

    if args.json:
        print(json.dumps(subs, ensure_ascii=False, separators=(',', ':')))
        return

    def label(k):
        return names.get(str(k)) or mnames.get(k) or ('#%s' % k)

    print('公共事件场景 %d 个，地图场景 %d 个' % (len(scenes), len(map_scenes)))
    print('嵌套（被别的场景播到）的场景：%d 个 -> 默认隐藏' % info['hidden'])
    print('剩余可见：%d + %d = %d' % (len(scenes) - info['hidden'], len(map_scenes),
                                      len(scenes) - info['hidden'] + len(map_scenes)))
    print()
    print('被调用次数 Top15：')
    rank = collections.Counter({t: len(v) for t, v in info['callers'].items()})
    for k, n in rank.most_common(15):
        print('   x%-3d %-24s <- %s' % (n, label(k)[:24],
                                        ', '.join(label(c)[:16] for c in info['callers'][k][:2])))
    if info['protected']:
        print()
        print('环保护（互相调用且无环外调用者，保留一个入口）：')
        for keep, comp in info['protected']:
            print('   保留 #%d %s ；隐藏 %s' % (keep, label(keep),
                                               ', '.join('#%d %s' % (x, label(x)) for x in comp if x != keep)))
    else:
        print()
        print('环保护：无（没有互相调用的场景）')


if __name__ == '__main__':
    main()
