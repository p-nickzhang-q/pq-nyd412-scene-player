#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""场景类型标签：h（含性内容）/ story（纯剧情、日常）/ misc（环境描述等杂项）。

【为什么用显式表而不是自动分类】
本作是成人游戏，**绝大多数场景本身就含性内容**（实测 `ZivaScene01` 是口交、
`VictoriaScene01-03` 全含、`TempleInitiationScene` 台词是「一场性快感的祭献」），
所以自动分类器无论怎么调都会把 80%+ 判成 h —— 而且会把 `Bed`/`怀孕`/`亲吻`
这类剧情里也常见的词误判。反过来，「纯剧情」是个小集合，可以逐条人工确认。

因此：
  - 默认 h；
  - `STORY_CE` / `MISC_CE`：逐条看过台词后确认的非 H 公共事件；
  - `MAP_TAGS`：80 个地图场景逐条看过台词 + 图片族的分类。

要改就改这几张表，改完重跑 `tools/setup.py` 即可。
"""

H, STORY, MISC = 'h', 'story', 'misc'

# 公共事件里确认「不含性内容」的（其余一律 h）
STORY_CE = {
    15, 16, 17,      # ShakalaEvent01-03：与 Shakala 初遇/战斗
    39, 41,          # Maghda × Dolf 01/03：地精剧情
    85,              # 被抓偷窥：偷窥被发现的过场
    117,             # Grug 受伤
    129, 130,        # 地穴白天 / 墓园夜晚：场景描写
    157,             # 水蛭袭击
    160,             # Caleah 初次约会
    202, 203,        # 龙：遭遇 / 战后
    228,             # Mia 林中相遇
    235,             # Mia 与祖母对峙
    264,             # Alice × Johan 桌边（酒馆谈生意）
    279,             # 归还传送石
    291,             # Victoria × 女儿（认亲）
    293,             # 女儿去游泳
    308,             # 与女儿组队
    333, 690,        # Rosy 面包店 02/03
    416,             # 探望 Victoria（产后）
    483,             # 观看地精女儿 阶段2
    487,             # 地精女儿 剧情01
    727,             # 酒馆掷骰
    754, 755,        # Tom 第一/二次输
    816,             # 使魔变身
    1063,            # Julia 第一次游泳
    1160,            # Obeah 被俘 下
    1394,            # 拜访酿酒姑娘们
    1781,            # 女儿 · 伏击之后
    1794, 1801,      # Baron 登场 / 训斥
    1804,            # 职责召唤
}

# 公共事件里确认「只是环境描述」的
MISC_CE = set()

# 地图场景（键 = "m<mapId>:<eventId>"）逐条分类
# h：图片族/台词确认含性内容
MAP_H = {
    'm1:81',    # 怪木林 → Victoria 怀孕H01 / 红色内衣 / 被抓偷窥
    'm6:6',     # 顶层 → 女儿床上1/2、小恶魔口交
    'm8:3',     # 魔法之井 → Liandra H2 / 怀孕H
    'm9:18',    # Shakala 森林回想（生子提议）
    'm13:32',   # 米娅遭骚扰 回想
    'm19:5',    # → Beth 求欢1/2
    'm19:9',    # StablesN3/N5 → Beth 马厩N6
    'm20:9',    # StablesN1/N2/N7（Beth 马厩）
    'm30:7',    # → Erevi 床上H / 绑在床上H
    'm32:23',   # → Shakala GD H01 / 林中H
    'm37:17',   # EreviWedding / TODBeforeMarriage（婚前夜）
    'm40:7',    # → Maghda 怀孕H1/H2
    'm53:37',   # → Ziva/Alice 群体 上
    'm61:61',   # → Caleah × Ziva H
    'm61:75',   # TempleBedroom2
    'm65:5',    # → Rosy 强制口交
    'm70:20',   # → 女儿床上2/3
    'm75:34',   # → Hilde 沐浴
    'm43:1',    # → Victoria×Gwynneth H
    'm95:87',   # AnnabelleYoungPreg
    'm105:23',  # → Adaobi 礼拜堂H
    'm106:17',  # → Reanna 军械库口交
    'm115:7',   # TODMaster（女儿）
    'm128:22',  # → Julia 谷仓婚礼
    'm130:7',   # → Julia 床上
    'm131:8',   # → Julia 床上
    'm140:62',  # 台词：可调节的性交凳
    'm153:67',  # 布里吉特引诱哥布林
    'm155:7',   # → Birgitte 小屋2 裸体/内衣
    'm156:22',  # BirgitteSunBathing
    'm156:34',  # → Hilde 沐浴
    'm156:35',  # → Freyja宴 骑乘
    'm156:41',  # → Freyja宴 骑乘
    'm166:1',   # → Naamah H1
    'm166:41',  # → Naamah H1/H2
    'm180:8',   # 灰港城堡 → Yvette 调教上/口交
    'm180:15',  # → Josephine/Yvette 泳池
    'm180:50',  # → Josephine/Yvette 泳池
}

# 地图场景里只是环境描述的
MAP_MISC = {
    'm8:2',     # 魔法之井：井的描写
    'm18:4',    # Frida 家：没人在家
    'm25:2',    # 恐惧之塔：门锁着
    'm46:41',   # 墓园：脚印
    'm97:9',    # 酒馆房间
    'm164:8',   # Daiyu 后台：已上锁
}

# 其余地图场景一律算 story（剧情/日常），例如北方森林袭击、决战内尔伽勒、
# 女祭司墓、蜘蛛洞、温泉、锦标赛、独角兽、Qetesh 宫殿等。


def ce_tag(event_id):
    if event_id in MISC_CE:
        return MISC
    if event_id in STORY_CE:
        return STORY
    return H


def map_tag(key):
    if key in MAP_MISC:
        return MISC
    if key in MAP_H:
        return H
    return STORY
