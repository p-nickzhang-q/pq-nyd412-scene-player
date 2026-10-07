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
import quest_names as QN  # noqa: E402

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


def loose_json(text):
    r"""任务参数里偶有非法转义（`\N[6]`），修一下再解析。"""
    return json.loads(re.sub(r'\\(?!["\\\\/bfnrtu])', r'\\\\', text))


def load_quests(www):
    """
    读 YEP_QuestJournal + YEP_X_MoreQuests1 里的任务定义（共 215 个）。
    任务编号就是剧情轴 —— 它和攻略里 `任务212：是个男孩` 的编号一致。
    """
    entries, _ = nesting.load_plugins(os.path.join(www, 'js', 'plugins.js'))
    quests = {}
    for e in entries:
        if 'Quest' not in (e.get('name') or ''):
            continue
        for k, v in (e.get('parameters') or {}).items():
            m = re.match(r'Quest (\d+)$', k)
            if not m or not str(v).strip():
                continue
            try:
                q = json.loads(v)
            except ValueError:
                try:
                    q = loose_json(v)
                except ValueError:
                    continue
            if isinstance(q, dict):
                quests[int(m.group(1))] = q
    return quests


def cjk_words(text, lo=2, hi=5):
    out = set()
    for run in re.findall(r'[\u4e00-\u9fff]+', text):
        for n in range(lo, hi + 1):
            for i in range(len(run) - n + 1):
                out.add(run[i:i + n])
    return out


def prepare_quests(quests):
    """预计算每个任务的文本、token 集合。"""
    out = {}
    for no, q in quests.items():
        title = str(q.get('Title', '') or '').strip()
        frm = str(q.get('From', '') or '').strip()
        loc = str(q.get('Location', '') or '').strip()
        desc = str(q.get('Description', '') or '')
        if isinstance(q.get('Description'), list):
            desc = ' '.join(str(x) for x in q['Description'])
        alltext = ' '.join([title, frm, loc, desc])
        cn = set()
        for run in re.findall(r'[\u4e00-\u9fff]{2,}', alltext):
            for n in (2, 3, 4):
                for i in range(len(run) - n + 1):
                    cn.add(run[i:i + n])
        out[no] = {'title': title, 'from': frm, 'loc': loc, 'desc': desc,
                   'all': alltext, 'low': alltext.lower(), 'concepts': cn,
                   'title_low': title.lower(), 'from_low': frm.lower(),
                   'loc_low': loc.lower(), 'desc_low': desc.lower()}
    return out


def camel(x):
    return [w.lower() for w in re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', str(x)) if len(w) >= 4]


def scene_signals(name, cmd_list, sw_name, var_name, extra_conds=()):
    """把一个场景拆成用于匹配任务的几组信号。"""
    head = head_of(name)
    sub = re.split(r'[ ·]', name)[1] if ' · ' in name else ''
    sub = re.sub(r'\d+', '', sub).strip(' （）()')

    alias = [head.lower()] + [a.lower() for a in QN.NAMES.get(head, [])]
    loc_alias = [head.lower()] + [a.lower() for a in QN.LOCATIONS.get(head, [])]

    pics, ids = [], []
    for c in cmd_list:
        code = c.get('code')
        p = c.get('parameters') or []
        if code == 231 and len(p) > 1:
            pics += camel(p[1])
        elif code == 111 and len(p) >= 2 and isinstance(p[1], int):
            ids.append(('s' if p[0] == 0 else 'v', p[1]))
    ids += [tuple(x) for x in extra_conds]

    req = []
    own = []
    head_low = head.lower()
    alts = [head_low] + [a.lower() for a in QN.NAMES.get(head, [])]
    for kind, i in sorted(set(ids)):
        nm = sw_name[i] if kind == 's' and 0 <= i < len(sw_name) else \
             (var_name[i] if kind == 'v' and 0 <= i < len(var_name) else '')
        req += camel(nm)
        if kind == 'v' and nm and any(a and a in nm.lower() for a in alts):
            own.append(i)
    # 只取变量 id（开关和变量是两套编号空间，混在一起排序没有意义）
    varids = [i for k_, i in ids if k_ == 'v']
    concepts = set()
    for t in req:
        for cn in QN.CONCEPTS.get(t, []):
            concepts.add(cn)
    return {'head': head, 'sub': sub, 'alias': alias, 'loc_alias': loc_alias,
            'subtok': cjk_words(sub), 'pics': pics, 'concepts': concepts, 'req': req,
            # 用「最大」而不是最小：一个场景会测多个变量，取最小容易被无关的低位变量带偏
            'own_max': max(own) if own else 999999,
            'var_max': max(varids) if varids else 999999}


def concept_weights(Q):
    """概念词 -> 权重。在越少的任务里出现，越能定位（类 IDF）。"""
    w = {}
    words = set()
    for q in Q.values():
        for cn in q['concepts']:
            words.add(cn)
    for cn in words:
        df = sum(1 for q in Q.values() if cn in q['all'])
        if df <= 2:
            w[cn] = 6
        elif df <= 5:
            w[cn] = 5
        elif df <= 12:
            w[cn] = 3
        elif df <= 25:
            w[cn] = 1
        else:
            w[cn] = 0          # 太泛（哥布林/悬赏/怀孕…），不参与定位
    return w


def score_quest(sig, q, cw):
    """场景与某个任务的契合度。分越高越像。"""
    s = 0
    sub = sig['sub']
    if sub and len(sub) >= 2:
        if sub in q['title']:
            s += 10
        elif sub in q['desc']:
            s += 3
    for a in sig['alias']:
        if a in q['from_low']:
            s += 5
        if a in q['title_low']:
            s += 3
        if a in q['desc_low']:
            s += 2
    for a in sig['loc_alias']:
        if a in q['loc_low']:
            s += 3
        if a in q['desc_low']:
            s += 1
    # 概念词要**和人物一起**出现在同一个任务里才算数 ——
    # 单看概念会到处误配（"怀孕"在几十个任务里都有），
    # 但「维多利亚 + 怀孕」这种组合就很能定位。
    char_here = any(a in q['low'] for a in sig['alias'])
    for cn in sig['concepts']:
        if cn not in q['all']:
            continue
        if char_here:
            s += max(cw.get(cn, 0), 2)
        elif cw.get(cn, 0) >= 5:
            s += cw[cn]
    for t in sig['pics']:
        if len(t) >= 5 and t in q['low']:
            s += 1
    return s


def compute(game_dir, verbose=False, scenes=None, map_scenes=None):
    """
    返回 {'order': [[场景键, 任务号], ...], 'chapters': [任务标题, ...], ...}。
    order 的顺序就是剧情顺序（未定位的排在最后）。
    """
    www = nesting.find_www(game_dir)
    game = os.path.dirname(www)
    quests = load_quests(www)
    if not quests:
        raise SystemExit('读不到任务定义（缺 YEP_QuestJournal？）')
    Q = prepare_quests(quests)
    CW = concept_weights(Q)

    if scenes is None or map_scenes is None:
        entries, _ = nesting.load_plugins(os.path.join(www, 'js', 'plugins.js'))
        sp = [e for e in entries if e.get('name') == 'ScenePlayer'][0]
        params = sp.get('parameters', {})
        if scenes is None:
            scenes = json.loads(params.get('sceneList') or '[]')
        if map_scenes is None:
            map_scenes = json.loads(params.get('mapScenes') or '[]')

    ce = json.load(open(os.path.join(www, 'data', 'CommonEvents.json'), encoding='utf-8'))
    by_id = {e['id']: e for e in ce if e}
    sysj = json.load(open(os.path.join(www, 'data', 'System.json'), encoding='utf-8'))
    sw_name = sysj.get('switches', [])
    var_name = sysj.get('variables', [])

    # 调用某公共事件的地图事件，其「页条件」也是这个场景的前置条件
    caller_conds = {}
    for fn in os.listdir(os.path.join(www, 'data')):
        if not re.match(r'Map\d+\.json$', fn):
            continue
        try:
            data = json.load(open(os.path.join(www, 'data', fn), encoding='utf-8'))
        except (IOError, ValueError):
            continue
        for ev in data.get('events', []):
            if not ev:
                continue
            for pg in ev.get('pages', []):
                c = pg.get('conditions') or {}
                ids = []
                for vk, ik in (('switch1Valid', 'switch1Id'), ('switch2Valid', 'switch2Id')):
                    if c.get(vk) and isinstance(c.get(ik), int):
                        ids.append(('s', c[ik]))
                if c.get('variableValid') and isinstance(c.get('variableId'), int):
                    ids.append(('v', c['variableId']))
                for cc in pg.get('list', []):
                    if cc.get('code') == 117 and cc.get('parameters'):
                        caller_conds.setdefault(cc['parameters'][0], []).extend(ids)

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ov_path = os.path.join(repo, 'params', 'storyOverrides.json')
    overrides = {}
    if os.path.isfile(ov_path):
        overrides = {str(k): v for k, v in json.load(open(ov_path, encoding='utf-8')).items()}

    rows = []
    for s in scenes:
        key, name = str(s[0]), s[1]
        e = by_id.get(s[0]) or {}
        sig = scene_signals(name, e.get('list', []), sw_name, var_name,
                            caller_conds.get(s[0], []))
        best, best_score = None, 0
        for no, q in Q.items():
            sc = score_quest(sig, q, CW)
            if sc > best_score or (sc == best_score and sc > 0 and best is not None and no < best):
                best, best_score = no, sc
        ch = best
        ev = []
        if best:
            ev.append('任务%d「%s」' % (best, Q[best]['title'][:14]))
            hitc = [cn for cn in sig['concepts'] if cn in Q[best]['all']]
            if hitc:
                ev.append('概念' + '、'.join(sorted(hitc)[:2]))
        rows.append({'key': key, 'kind': 'ce', 'id': s[0], 'name': name, 'ord_id': s[0],
                     'line': line_of(name), 'chapter': ch, 'evidence': ev,
                     'sub': suffix_no(name), 'score': best_score,
                     'own_max': sig['own_max'], 'var_max': sig['var_max']})

    # 地图场景（若收录）：用地图官方名/图片名定位，并用它调用的公共事件的任务号作下界
    ce_ch = {r['key']: r['chapter'] for r in rows if r['kind'] == 'ce'}
    map_info = {m['id']: m['name'] for m in
                json.load(open(os.path.join(www, 'data', 'MapInfos.json'), encoding='utf-8')) if m}
    for m in map_scenes:
        key = 'm%d:%d' % (m[0], m[1])
        name = m[4]
        lst = nesting.map_event_list(www, m[0], m[1]) or []
        sig = scene_signals(name, lst, sw_name, var_name, caller_conds.get(-1, []))
        off = map_info.get(m[0])
        if off:
            sig['alias'] = sig['alias'] + [off.lower()]
            sig['loc_alias'] = sig['loc_alias'] + [off.lower()]
        best, best_score = None, 0
        for no, q in Q.items():
            sc = score_quest(sig, q, CW)
            if sc > best_score:
                best, best_score = no, sc
        called = [ce_ch[str(c['parameters'][0])] for c in lst
                  if c.get('code') == 117 and c.get('parameters')
                  and str(c['parameters'][0]) in ce_ch and ce_ch[str(c['parameters'][0])]]
        ch = best
        ev = []
        if best:
            ev.append('任务%d「%s」' % (best, Q[best]['title'][:14]))
        rows.append({'key': key, 'kind': 'map', 'id': key, 'name': name,
                     'ord_id': m[0] * 10000 + m[1], 'line': line_of(name),
                     'chapter': ch, 'evidence': ev, 'sub': m[1], 'score': best_score,
                     'own_min': sig['own_min'], 'all_min': sig['all_min']})

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
    # 同一任务内：先按人物组（该组最早事件 id，尊重创建顺序），再子线、编号、id
    gmin = {}
    for r in placed:
        k = (r['chapter'], head_of(r['name']))
        gmin[k] = min(gmin.get(k, 1 << 30), r['ord_id'])
    # 同一个任务里：先按人物分组（尊重作者创建顺序），
    # 组内按「人物专属变量 id -> 全部变量 id」排 —— 作者写场景的顺序基本跟着剧情走
    # （实测 Victoria: 134 剧情01~03 -> 199 怀孕 -> 344 自慰/剧情灵药 -> 419 内衣怀孕）。
    placed.sort(key=lambda r: (r['chapter'], gmin[(r['chapter'], head_of(r['name']))],
                               r['own_max'], r['var_max'], r['line'], r['sub'], r['ord_id']))
    unplaced.sort(key=lambda r: r['ord_id'])
    if verbose:
        print('任务定义 %d 个，已定位 %d / %d，未定位 %d'
              % (len(quests), len(placed), len(rows), len(unplaced)))
    return {'order': [[r['key'], r['chapter']] for r in placed + unplaced],
            'chapters': chapters_array(Q),
            'placed': len(placed),
            'unplaced': [r['key'] for r in unplaced],
            'rows': placed + unplaced}


def chapters_array(Q):
    """按任务号定位的标题数组（索引 = 任务号 - 1）。"""
    arr = [''] * (max(Q) if Q else 0)
    for n, q in Q.items():
        arr[n - 1] = ('%d %s' % (n, q['title'])).strip()
    return arr


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
