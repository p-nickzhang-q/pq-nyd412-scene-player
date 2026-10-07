#!/usr/bin/env python3
"""
按剧情顺序给场景排序。

依据：游戏自带的中文攻略 ——
  * `Walkthroughs/PQ_NYD_v3.71_full_walkthrough.zh.md` 第 12 节有约 188 个任务，
    **是按剧情推进顺序写的**；
  * 之后的补丁攻略（NYD375/381/391/395/401/410）是 186~215 号任务，按版本顺序接在后面。
把它们拼成 1..215 的「剧情章节表」，再给每个场景定一个章节号：

  1. **人物/地点**：取场景名的第一个词（"Frida · 调情" → Frida），
     在攻略里找**首次出现**的章节 —— 这就是这条人物线的起点。
  2. **前置条件**：场景自己的条件判断（指令 111）里引用的开关/变量，
     名字本身就带任务标识（如 `CathrineNoCurse`、`FreyjaQuest`、`MammaeMajorisActive`），
     拆成单词后同样去攻略里定位。
  3. 最终章节 = max(人物线起点, 最晚的前置条件章节) ——
     一个场景不可能出现在它的前置条件之前。
  4. 同一个章节内：按名字里的编号（"剧情01" → 01）再按事件 id。

定位不到的场景排在最后（按 id），并在报告里单列，方便手工订正。

手工订正：`params/storyOverrides.json`，形如 `{"1635": 196, "m156:35": 210}`
（键 = 场景键，值 = 章节号；给 `null` 表示强制放到最后）。优先级最高。

用法：
    python3 tools/story_order.py "/path/to/游戏"            # 报告
    python3 tools/story_order.py "/path/to/游戏" --json      # 输出插件参数 JSON
    python3 tools/story_order.py "/path/to/游戏" --md        # 生成 STORY_ORDER.md
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nesting  # noqa: E402

# 顺序 = 剧情顺序：全文攻略在前，补丁攻略按版本递增接在后面
WALKTHROUGHS = [
    ('PQ_NYD_v3.71_full_walkthrough.zh.md', '第12节'),
    ('Walkthrough NYD375.zh.md', None),
    ('Walkthrough NYD381.zh.md', None),
    ('Walkthrough NYD391.zh.md', None),
    ('Walkthrough NYD395.zh.md', None),
    ('Walkthrough NYD401.zh.md', None),
    ('Walkthrough NYD410.zh.md', None),
]

# 我们的场景名用词 -> 攻略里的说法。
# 攻略和事件名对同一地点的译法经常不同（我们是"北方森林"，攻略是"北部森林"），
# 不做映射就会有一批场景定位不到。
SYNONYMS = {
    '北方森林': ['北部森林', 'Northern Forest'],
    '怪木林': ['Weirdwood'],
    '魔法之井': ['圣井'],
    '沙卡拉斯村': ['哥布林村庄', 'Shakala'],
    '灰港城堡': ['Greyport'],
    '灰港': ['Greyport'],
    '内城': ['Greyport', '内城'],
    '男爵城堡': ['男爵'],
    '酒馆一楼': ['旅店'],
    '跳跃的驴子': ['旅店'],
    '格蕾塔和米娅': ['Greta'],
    '巨人的村庄': ['巨人'],
    '地精女儿': ['Female Goblin'],
    '观看地精女儿': ['Female Goblin'],
    '蜘蛛娘': ['蜘蛛'],
    '地牢装置': ['地牢'],
}

# 拆开关/变量名时丢掉这些没有区分度的词
STOPWORDS = {
    'quest', 'active', 'complete', 'completed', 'done', 'stage', 'part', 'intro',
    'start', 'started', 'value', 'count', 'time', 'day', 'event', 'scene', 'flag',
    'check', 'talk', 'talked', 'met', 'seen', 'have', 'has', 'got', 'get', 'the',
    'and', 'with', 'for', 'not', 'yes', 'no', 'first', 'second', 'third', 'after',
    'before', 'again', 'unlock', 'unlocked', 'true', 'false', 'open', 'opened',
    'find', 'found', 'give', 'gave', 'new', 'old', 'test', 'set', 'clear', 'reset',
}


def load_chapters(wt_dir):
    """把攻略里的任务小节按剧情顺序拼成章节表。"""
    chapters = []
    for fname, anchor in WALKTHROUGHS:
        path = os.path.join(wt_dir, fname)
        if not os.path.isfile(path):
            continue
        text = open(path, encoding='utf-8').read()
        if anchor:
            i = text.find('## ' + anchor)
            if i >= 0:
                text = text[i:]
        parts = re.split(r'^###\s*(.+)$', text, flags=re.M)
        # parts = [前言, 标题1, 正文1, 标题2, 正文2, ...]
        for k in range(1, len(parts) - 1, 2):
            title = parts[k].strip()
            body = parts[k + 1]
            if title.startswith('任务') or '任务' in title:
                chapters.append({'title': title, 'text': title + '\n' + body,
                                 'from': fname})
    return chapters


def camel_tokens(name):
    """'CathrineNoCurse' -> ['cathrine', 'curse']；过滤无区分度的词。"""
    if not name:
        return []
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+', str(name))
    out = []
    for w in words:
        w = w.strip()
        if len(w) < 4 or w.isdigit():
            continue
        if w.lower() in STOPWORDS:
            continue
        out.append(w)
    return out


def cond_switches(cmd_list):
    """场景里条件判断（111）引用到的开关/变量 id。"""
    sw, va = set(), set()
    for c in cmd_list:
        if c.get('code') != 111:
            continue
        p = c.get('parameters') or []
        if len(p) < 2 or not isinstance(p[1], int):
            continue
        if p[0] == 0:
            sw.add(p[1])
        elif p[0] == 1:
            va.add(p[1])
    return sw, va


def head_of(name):
    return re.split(r'[ ·×（(]', name)[0].strip()


def is_entity(tok, entities):
    """有同义词映射的词一律当实体（那是人工确认过的对应关系）。"""
    if tok in SYNONYMS:
        return True
    """
    够具体才当信号：
      * 中文 ≥3 字（"蝙蝠洞"、"地精女儿"）；
      * 英文 ≥4 字母（"Victoria"）；
      * 或者它是**反复出现的实体**（在我们的场景名里出现 ≥2 次，如"女儿"）。
    这样能挡掉「解锁」「归还传送石」这类一次性的描述性名字。
    """
    if tok in entities:
        return True
    if re.search(r'[A-Za-z]', tok):
        return len(tok) >= 4
    return len(tok) >= 3


def name_tokens(name, orig='', entities=()):
    """场景名 -> 用于在攻略里搜索的词（只留够具体的）。"""
    out = []
    head = head_of(name)
    if is_entity(head, entities):
        out.append(head)
    for part in name.split('×'):
        p = re.split(r'[ ·（(]', part.strip())[0].strip()
        if p != head and is_entity(p, entities) and p not in out:
            out.append(p)
    if orig:
        for w in camel_tokens(orig):
            if w.lower() not in [x.lower() for x in out]:
                out.append(w)
    return out


def line_of(name):
    """子线名：去掉数字后的名字（"Victoria · 剧情01" -> "Victoria · 剧情"），
    用来让同一人物的不同子线各自聚在一起，不互相穿插。"""
    return re.sub(r'\d+', '', name)


def suffix_no(name):
    """名字里的编号，用来在章节内排序："剧情02" -> 2，"帐篷3 后门" -> 3。"""
    m = re.search(r'(\d+)', name)
    return int(m.group(1)) if m else 999


def cjk_ngrams(text, lo=2, hi=4):
    """把中文长串切成 2~4 字的片段（"蜘蛛洞剧情3" -> 蜘蛛洞、蜘蛛洞剧…）。"""
    out = set()
    for run in re.findall(r'[\u4e00-\u9fff]+', text):
        for n in range(lo, hi + 1):
            for i in range(0, len(run) - n + 1):
                out.add(run[i:i + n])
    return out


def build_index(chapters):
    """词 -> 首次出现的章节号（1 起）。英文按词切，中文切 2~4 字片段。"""
    idx = {}

    def add(tok, no):
        k = tok.lower()
        if k and k not in idx:
            idx[k] = no

    for i, ch in enumerate(chapters, 1):
        text = ch['title'] + '\n' + ch['text']
        for tok in set(re.findall(r'[A-Za-z]{3,}', text)):
            if tok.lower() in STOPWORDS:
                continue
            add(tok, i)
        for tok in cjk_ngrams(text):
            add(tok, i)
    return idx


def chapter_of(tokens, idx):
    """
    返回 (最早章节号, 命中的词)。
    中文长词先整词查，查不到再切成 3~4 字片段（**不切 2 字**：
    "第一层酒馆" 切成 "第一" 会误配到第 1 章）。候选按「长度降序、字典序」排，
    保证跨进程结果一致（不能依赖 set 的迭代顺序）。
    """
    hits = []
    for t in tokens:
        if re.search(r'[A-Za-z]', t):
            probes = [t]
        else:
            probes = [t] + sorted(cjk_ngrams(t, 3, 4), key=lambda x: (-len(x), x))
        # 我们的用词 -> 攻略用词
        for alt in SYNONYMS.get(t, []):
            probes = probes + ([alt] if re.search(r'[A-Za-z]', alt) else
                               [alt] + sorted(cjk_ngrams(alt, 3, 4), key=lambda x: (-len(x), x)))
        for probe in probes:
            k = probe.lower()
            if k in idx:
                hits.append((idx[k], probe))
                break
    if not hits:
        return None, None
    return min(hits)


def compute(game_dir, verbose=False):
    """
    返回 {'order': [[场景键, 章节号], ...], 'chapters': [标题, ...], ...}。
    order 的顺序就是剧情顺序（未定位的排在最后）。
    """
    www = nesting.find_www(game_dir)
    game = os.path.dirname(www)
    chapters = load_chapters(os.path.join(game, 'Walkthroughs'))
    if not chapters:
        raise SystemExit('读不到任何任务小节（缺 Walkthroughs/*.zh.md？）')
    idx = build_index(chapters)

    entries, _ = nesting.load_plugins(os.path.join(www, 'js', 'plugins.js'))
    sp = [e for e in entries if e.get('name') == 'ScenePlayer'][0]
    params = sp.get('parameters', {})
    scenes = json.loads(params.get('sceneList') or '[]')
    map_scenes = json.loads(params.get('mapScenes') or '[]')

    ce = json.load(open(os.path.join(www, 'data', 'CommonEvents.json'), encoding='utf-8'))
    by_id = {e['id']: e for e in ce if e}
    sysj = json.load(open(os.path.join(www, 'data', 'System.json'), encoding='utf-8'))
    sw_name = sysj.get('switches', [])
    var_name = sysj.get('variables', [])
    map_info = {m['id']: m['name'] for m in
                json.load(open(os.path.join(www, 'data', 'MapInfos.json'), encoding='utf-8')) if m}

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ov_path = os.path.join(repo, 'params', 'storyOverrides.json')
    overrides = {}
    if os.path.isfile(ov_path):
        overrides = {str(k): v for k, v in json.load(open(ov_path, encoding='utf-8')).items()}

    heads = collections.Counter(head_of(x[1]) for x in scenes)
    heads.update(head_of(m[4]) for m in map_scenes)
    entities = {h for h, c in heads.items() if c >= 2 and len(h) >= 2}

    rows = []
    for s in scenes:
        key, name = str(s[0]), s[1]
        orig = s[2] if len(s) > 2 else ''
        e = by_id.get(s[0]) or {}
        sw, va = cond_switches(e.get('list', []))
        req_tokens = []
        for i_ in sorted(sw):
            req_tokens += camel_tokens(sw_name[i_] if i_ < len(sw_name) else '')
        for i_ in sorted(va):
            req_tokens += camel_tokens(var_name[i_] if i_ < len(var_name) else '')
        pics = []
        for c in (e.get('list') or []):
            if c.get('code') == 231 and len(c.get('parameters') or []) > 1:
                for w in camel_tokens(c['parameters'][1]):
                    if w.lower() not in [x.lower() for x in pics]:
                        pics.append(w)

        nm_ch, nm_tok = chapter_of(name_tokens(name, orig, entities), idx)
        rq_ch, rq_tok = chapter_of(req_tokens, idx)
        pc_ch, pc_tok = chapter_of(pics, idx)
        base = nm_ch or pc_ch
        lower = rq_ch or pc_ch
        ch = max(base, lower) if (base and lower) else (base or lower)
        evidence = []
        if nm_tok:
            evidence.append('名字「%s」' % nm_tok)
        if rq_tok:
            evidence.append('前置「%s」' % rq_tok)
        if pc_tok and not nm_tok:
            evidence.append('图片「%s」' % pc_tok)
        rows.append({'key': key, 'kind': 'ce', 'id': s[0], 'name': name, 'ord_id': s[0],
                     'line': line_of(name), 'chapter': ch, 'evidence': evidence,
                     'sub': suffix_no(name)})

    ce_chapter = {r['key']: r['chapter'] for r in rows if r['kind'] == 'ce'}
    listed = {str(x[0]) for x in scenes}
    for m in map_scenes:
        key = 'm%d:%d' % (m[0], m[1])
        name = m[4]
        toks = []
        loc = re.split(r'[ ·]', name)[0].strip()
        if not (loc.startswith('Map') and loc[3:].isdigit()):
            toks.append(loc)
        off = map_info.get(m[0])
        if off and off not in toks:
            toks.append(off)
        lst = nesting.map_event_list(www, m[0], m[1]) or []
        for c in lst:
            if c.get('code') == 231 and len(c.get('parameters') or []) > 1:
                for w in camel_tokens(c['parameters'][1]):
                    if w.lower() not in [x.lower() for x in toks]:
                        toks.append(w)
        nm_ch, nm_tok = chapter_of([t for t in toks if is_entity(t, entities) or
                                    re.search(r'[A-Za-z]', t)], idx)
        called = []
        for c in lst:
            if c.get('code') == 117:
                pp = c.get('parameters') or []
                if pp and str(pp[0]) in listed and ce_chapter.get(str(pp[0])):
                    called.append(ce_chapter[str(pp[0])])
        lower = max(called) if called else None
        ch = max([x for x in (nm_ch, lower) if x]) if (nm_ch or lower) else None
        ev = []
        if nm_tok:
            ev.append('地点「%s」' % nm_tok)
        if lower:
            ev.append('调用场景的章节 %d' % lower)
        rows.append({'key': key, 'kind': 'map', 'id': key, 'name': name,
                     'ord_id': m[0] * 10000 + m[1], 'line': line_of(name),
                     'chapter': ch, 'evidence': ev, 'sub': m[1]})

    # 还没定位的：如果它被某个已定位的场景调用（是子场景），就跟着调用者
    subs, _info = nesting.analyze(www, scenes, map_scenes)
    by_key = {r['key']: r for r in rows}
    for r in rows:
        if r['chapter']:
            continue
        callers = subs.get(r['key']) or []
        chs = [by_key[str(c)]['chapter'] for c in callers
               if str(c) in by_key and by_key[str(c)]['chapter']]
        if chs:
            r['chapter'] = max(chs)
            r['evidence'] = ['跟随调用者 %s' % '、'.join(str(c) for c in callers[:2])]

    for r in rows:
        if r['key'] in overrides:
            r['chapter'] = overrides[r['key']]
            r['evidence'] = ['手工订正']

    placed = [r for r in rows if r['chapter']]
    unplaced = [r for r in rows if not r['chapter']]
    # 章节内：先按「人物组」（用该组最早的事件 id，尊重作者创建顺序），
    # 再按子线名、名字里的编号、事件 id。
    gmin = {}
    for r in placed:
        k = (r['chapter'], head_of(r['name']))
        gmin[k] = min(gmin.get(k, 1 << 30), r['ord_id'])
    placed.sort(key=lambda r: (r['chapter'], gmin[(r['chapter'], head_of(r['name']))],
                               r['line'], r['sub'], r['ord_id']))
    unplaced.sort(key=lambda r: r['ord_id'])
    if verbose:
        print('攻略章节 %d 个，已定位 %d / %d，未定位 %d'
              % (len(chapters), len(placed), len(rows), len(unplaced)))
    return {'order': [[r['key'], r['chapter']] for r in placed + unplaced],
            'chapters': [c['title'] for c in chapters],
            'placed': len(placed),
            'unplaced': [r['key'] for r in unplaced],
            'rows': placed + unplaced}


def md_lines(chapters, rows):
    out = ['# 剧情顺序（storyOrder）\n',
           '依据游戏自带中文攻略的任务顺序（%d 个章节）给场景定位，' % len(chapters),
           '由 `tools/story_order.py` 生成。\n',
           '章节内按人物组、子线名、名字编号排序；定位不到的排在最后，'
           '可在 `params/storyOverrides.json` 里手工订正。\n',
           '| 顺序 | 剧情章节 | 章节标题 | 场景 | 定位依据 |',
           '|---|---|---|---|---|']
    for n, r in enumerate(rows, 1):
        ch = r['chapter']
        title = chapters[ch - 1] if ch and ch <= len(chapters) else '（未定位）'
        out.append('| %d | %s | %s | %s `%s` | %s |' % (
            n, ch if ch else '—', title, r['name'], r['key'],
            '、'.join(r['evidence']) or '—'))
    return out


def main():
    ap = argparse.ArgumentParser(description='按剧情顺序给场景排序')
    ap.add_argument('game_dir')
    ap.add_argument('--json', action='store_true', help='输出 {order, chapters} JSON')
    ap.add_argument('--md', action='store_true', help='生成 STORY_ORDER.md')
    args = ap.parse_args()

    res = compute(args.game_dir, verbose=not (args.json or args.md))
    if args.json:
        print(json.dumps({'order': res['order'], 'chapters': res['chapters']},
                         ensure_ascii=False, separators=(',', ':')))
        return
    if args.md:
        print('\n'.join(md_lines(res['chapters'], res['rows'])))
        return
    rows = res['rows']
    bych = collections.OrderedDict()
    for r in rows:
        if r['chapter']:
            bych.setdefault(r['chapter'], []).append(r)
    print('未定位  : %d 个（排在最后）%s' % (
        len(res['unplaced']), '：' + '、'.join(res['unplaced'][:8]) if res['unplaced'] else ''))
    print()
    print('=== 章节分布（前 30 章）===')
    for no, items in list(bych.items())[:30]:
        title = res['chapters'][no - 1] if no <= len(res['chapters']) else '?'
        print('  %3d  %-28s %2d 个: %s' % (no, title[:28], len(items),
              '、'.join(i['name'][:13] for i in items[:4])))


if __name__ == '__main__':
    main()
