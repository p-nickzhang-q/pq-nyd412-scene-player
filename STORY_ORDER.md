# 剧情顺序（storyOrder）

依据游戏自带中文攻略的任务顺序（219 个章节）给场景定位，
由 `tools/story_order.py` 生成。

章节内按人物组、子线名、名字编号排序；定位不到的排在最后，可在 `params/storyOverrides.json` 里手工订正。

| 顺序 | 剧情章节 | 章节标题 | 场景 | 定位依据 |
|---|---|---|---|---|
| 1 | 3 | 任务：与所有村民交谈 | Alice · TF 变身 `2001` | 名字「Alice」、前置「Alice」 |
| 2 | 3 | 任务：与所有村民交谈 | Alice · 书库 H `262` | 名字「Alice」、前置「Alice」 |
| 3 | 3 | 任务：与所有村民交谈 | Alice · 厨房 H `261` | 名字「Alice」、前置「Alice」 |
| 4 | 3 | 任务：与所有村民交谈 | Alice · 她的房间 `256` | 名字「Alice」、前置「Alice」 |
| 5 | 3 | 任务：与所有村民交谈 | Alice · 房间 灵药 `268` | 名字「Alice」 |
| 6 | 3 | 任务：与所有村民交谈 | Alice · 神龛 H `260` | 名字「Alice」、前置「Alice」 |
| 7 | 3 | 任务：与所有村民交谈 | Alice · 约会 `266` | 名字「Alice」 |
| 8 | 3 | 任务：与所有村民交谈 | Alice · 群体 上 `807` | 名字「Alice」、前置「Alice」 |
| 9 | 3 | 任务：与所有村民交谈 | Alice · 试衣间 `255` | 名字「Alice」、前置「Alice」 |
| 10 | 3 | 任务：与所有村民交谈 | Alice · 酿酒 H `1261` | 名字「Alice」、前置「Alice」 |
| 11 | 3 | 任务：与所有村民交谈 | Alice · 锁链1 `1492` | 名字「Alice」、前置「Alice」 |
| 12 | 3 | 任务：与所有村民交谈 | Alice · 锁链2 `1493` | 名字「Alice」、前置「Alice」 |
| 13 | 3 | 任务：与所有村民交谈 | Alice × Johan 桌边 `264` | 名字「Alice」、前置「Alice」 |
| 14 | 3 | 任务：与所有村民交谈 | 女儿 · 伏击之后 `1781` | 名字「女儿」 |
| 15 | 3 | 任务：与所有村民交谈 | 女儿 · 床上3 `298` | 名字「女儿」 |
| 16 | 3 | 任务：与所有村民交谈 | Gwynneth · 宅邸2 H `459` | 名字「Gwynneth」、前置「Gwynneth」 |
| 17 | 3 | 任务：与所有村民交谈 | Gwynneth · 家中（灵药） `1259` | 名字「Gwynneth」、前置「Gwynneth」 |
| 18 | 3 | 任务：与所有村民交谈 | Gwynneth · 床上 H `1258` | 名字「Gwynneth」、前置「Gwynneth」 |
| 19 | 3 | 任务：与所有村民交谈 | Victoria×Gwynneth · H（大场景） `1257` | 名字「Gwynneth」、前置「Gwynneth」 |
| 20 | 3 | 任务：与所有村民交谈 | Beth · 床上 `1490` | 名字「Beth」、前置「Beth」 |
| 21 | 3 | 任务：与所有村民交谈 | Beth · 求欢2 `1557` | 名字「Beth」、前置「Beth」 |
| 22 | 3 | 任务：与所有村民交谈 | Beth · 求欢1（大场景） `1556` | 名字「Beth」、前置「Beth」 |
| 23 | 3 | 任务：与所有村民交谈 | Beth · 马厩 N6 `1488` | 名字「Beth」、前置「Beth」 |
| 24 | 4 | 任务：失踪的货物 | Maghda · 怀孕 H1 `395` | 名字「Maghda」、前置「Maghda」 |
| 25 | 4 | 任务：失踪的货物 | Maghda · 怀孕 H2 `397` | 名字「Maghda」、前置「Maghda」 |
| 26 | 4 | 任务：失踪的货物 | Maghda · 怀孕 H3 `400` | 名字「Maghda」 |
| 27 | 4 | 任务：失踪的货物 | Maghda · 洞中 H `1255` | 名字「Maghda」、前置「Maghda」 |
| 28 | 4 | 任务：失踪的货物 | Maghda · 洞外 H `1256` | 名字「Maghda」、前置「Dolf」 |
| 29 | 4 | 任务：失踪的货物 | Maghda × Dolf 02 `40` | 名字「Dolf」 |
| 30 | 4 | 任务：失踪的货物 | Maghda × Dolf 03 `41` | 名字「Dolf」、前置「Maghda」 |
| 31 | 4 | 任务：失踪的货物 | Maghda × Dolf 04 `386` | 名字「Dolf」 |
| 32 | 4 | 任务：失踪的货物 | Maghda × Dolf 05 `1356` | 名字「Dolf」、前置「Dolf」 |
| 33 | 4 | 任务：失踪的货物 | Erevi · 黑色礼服（灵药） `653` | 名字「Potion」 |
| 34 | 4 | 任务：失踪的货物 | Erevi × 女儿 `304` | 名字「女儿」、前置「Potion」 |
| 35 | 4 | 任务：失踪的货物 | Liandra · H2 灵药 `347` | 名字「Potion」 |
| 36 | 4 | 任务：失踪的货物 | 观看地精女儿 阶段1 `482` | 图片「Goblin」 |
| 37 | 4 | 任务：失踪的货物 | 观看地精女儿 阶段2 `483` | 图片「Goblin」 |
| 38 | 4 | 任务：失踪的货物 | 地精女儿 · 剧情01 `487` | 图片「Goblin」 |
| 39 | 4 | 任务：失踪的货物 | 地精女儿 · 剧情02 `488` | 前置「Goblin」、图片「Goblin」 |
| 40 | 4 | 任务：失踪的货物 | 地精女儿 · 剧情03 `489` | 前置「Goblin」、图片「Goblin」 |
| 41 | 4 | 任务：失踪的货物 | Shakala · 林中 H `503` | 名字「Forest」 |
| 42 | 4 | 任务：失踪的货物 | 地穴 H（灵药·大场景） `685` | 名字「Potion」 |
| 43 | 4 | 任务：失踪的货物 | 使魔 · 变身 `816` | 图片「Forest」 |
| 44 | 5 | 任务：哥布林耳朵 | Shakala · GD H01 `497` | 名字「Shakala」、前置「Goblin」 |
| 45 | 5 | 任务：哥布林耳朵 | Shakala · 事件01 `15` | 名字「Shakala」 |
| 46 | 5 | 任务：哥布林耳朵 | Shakala · 事件02 `16` | 名字「Shakala」、前置「Shakala」 |
| 47 | 5 | 任务：哥布林耳朵 | Shakala · 事件03 `17` | 名字「Shakala」 |
| 48 | 5 | 任务：哥布林耳朵 | Shakala · 婚礼 上 `67` | 名字「Shakala」 |
| 49 | 5 | 任务：哥布林耳朵 | Shakala · 婚礼双人 `504` | 名字「Shakala」 |
| 50 | 5 | 任务：哥布林耳朵 | Shakala · 桌上 H `1151` | 名字「Shakala」、前置「Shakala」 |
| 51 | 7 | 任务：望远镜 | Maghda × Dolf 01 `39` | 名字「Dolf」 |
| 52 | 10 | 任务：Witch Trouble | 神殿 · 入会仪式 `125` | 名字「Temple」 |
| 53 | 10 | 任务：Witch Trouble | Caleah × Ziva H（大场景） `214` | 名字「Ziva」、前置「Potion」 |
| 54 | 10 | 任务：Witch Trouble | 蜘蛛娘 · 杂交 H `518` | 名字「Spider」、前置「Spider」 |
| 55 | 10 | 任务：Witch Trouble | 蜘蛛娘 · 阶段0 `514` | 名字「Spider」 |
| 56 | 10 | 任务：Witch Trouble | 蜘蛛娘 · 阶段1 `515` | 名字「Spider」 |
| 57 | 10 | 任务：Witch Trouble | 被蜘蛛娘抓住 `520` | 名字「Spider」 |
| 58 | 10 | 任务：Witch Trouble | 蜘蛛洞 · 剧情3B `526` | 名字「Spider」、前置「Spider」 |
| 59 | 10 | 任务：Witch Trouble | Oksana · 神殿 H（灵药） `683` | 名字「Temple」 |
| 60 | 10 | 任务：Witch Trouble | Ziva · TF 变身 `2003` | 名字「Ziva」、前置「Ziva」 |
| 61 | 10 | 任务：Witch Trouble | Ziva · 群体 上 `806` | 名字「Ziva」、前置「Alice」 |
| 62 | 10 | 任务：Witch Trouble | 女儿 · 地牢玩具 `1251` | 名字「女儿」、前置「Nergal」 |
| 63 | 10 | 任务：Witch Trouble | 告诉Gabriel关于Beth `1477` | 名字「Beth」、前置「Temple」 |
| 64 | 10 | 任务：Witch Trouble | Qetesh · 喷泉 `1491` | 名字「Qetesh」、前置「Qetesh」 |
| 65 | 10 | 任务：Witch Trouble | Qetesh · 宫殿1 `1837` | 名字「Qetesh」、前置「Qetesh」 |
| 66 | 10 | 任务：Witch Trouble | Qetesh · 宫殿2 `1838` | 名字「Qetesh」、前置「Qetesh」 |
| 67 | 10 | 任务：Witch Trouble | Qetesh · 床上 `1829` | 名字「Qetesh」、前置「Qetesh」 |
| 68 | 11 | 任务：Sacred Water | Liandra · H2 `340` | 名字「Liandra」 |
| 69 | 11 | 任务：Sacred Water | Liandra · 井边 H `1166` | 名字「Liandra」 |
| 70 | 11 | 任务：Sacred Water | Liandra · 井边口交 `1165` | 名字「Liandra」 |
| 71 | 11 | 任务：Sacred Water | Liandra · 井边脱衣 `1164` | 名字「Liandra」 |
| 72 | 11 | 任务：Sacred Water | Liandra · 卧室 H `990` | 名字「Liandra」、前置「Liandra」 |
| 73 | 11 | 任务：Sacred Water | Liandra · 床上裸体 H `989` | 名字「Liandra」、前置「Liandra」 |
| 74 | 11 | 任务：Sacred Water | Liandra · 怀孕 H `341` | 名字「Liandra」 |
| 75 | 11 | 任务：Sacred Water | Liandra · 花园 `978` | 名字「Liandra」、前置「Liandra」 |
| 76 | 11 | 任务：Sacred Water | Lu × Li 三人行 `1087` | 前置「Liandra」 |
| 77 | 11 | 任务：Sacred Water | Caleah · 酿酒 H `1260` | 名字「Wine」、前置「Alice」 |
| 78 | 11 | 任务：Sacred Water | 拜访酿酒姑娘们 `1394` | 名字「Wine」、前置「Alice」 |
| 79 | 12 | 任务：租房 | Victoria · 剧情01 `103` | 名字「Victoria」、前置「Victoria」 |
| 80 | 12 | 任务：租房 | Victoria · 剧情02 `106` | 名字「Victoria」、前置「Potion」 |
| 81 | 12 | 任务：租房 | Victoria · 剧情03 `107` | 名字「Victoria」、前置「Potion」 |
| 82 | 12 | 任务：租房 | Victoria · 怀孕 H01 `139` | 名字「Victoria」、前置「Victoria」 |
| 83 | 12 | 任务：租房 | Victoria · 蓝色服装 `1834` | 名字「Victoria」、前置「Victoria」 |
| 84 | 12 | 任务：租房 | Victoria · 裸体 `452` | 名字「Victoria」、前置「Victoria」 |
| 85 | 18 | 任务：The Temple of Qetesh | Grug · 受伤 `117` | 名字「Grug」 |
| 86 | 18 | 任务：The Temple of Qetesh | Oksana · 神殿卧室3 H `1051` | 名字「Temple」、前置「Heal」 |
| 87 | 22 | 任务：哥布林炼金术 | Erevi · 灵药受孕 `169` | 名字「Spirit」 |
| 88 | 22 | 任务：哥布林炼金术 | ED · 课程 `1823` | 前置「Potions」 |
| 89 | 25 | 任务：拯救小狗！ | Frida · 帐篷口交（灵药） `378` | 名字「Potion」 |
| 90 | 25 | 任务：拯救小狗！ | Frida · 床上 H（怀孕） `88` | 名字「Frida」 |
| 91 | 25 | 任务：拯救小狗！ | Frida · 床上 H（未孕） `87` | 名字「Frida」、前置「Frida」 |
| 92 | 25 | 任务：拯救小狗！ | Frida · 调情 `13` | 名字「Frida」、前置「Frida」 |
| 93 | 25 | 任务：拯救小狗！ | Freyja宴 · Frida 未中 `1485` | 名字「Frida」、前置「Frida」 |
| 94 | 25 | 任务：拯救小狗！ | Freyja宴 · Frida 骑乘 `1482` | 名字「Frida」、前置「Frida」 |
| 95 | 26 | 任务：Recovering the Crystal | Ziva · 剧情01 `10` | 名字「Ziva」 |
| 96 | 26 | 任务：Recovering the Crystal | Mia · 与祖母对峙 `235` | 名字「Mia」 |
| 97 | 26 | 任务：Recovering the Crystal | Mia · 口交 `66` | 名字「Mia」 |
| 98 | 26 | 任务：Recovering the Crystal | Mia · 接吻 `63` | 名字「Mia」 |
| 99 | 26 | 任务：Recovering the Crystal | Mia · 私处 `65` | 名字「Mia」 |
| 100 | 26 | 任务：Recovering the Crystal | Mia · 胸部 `64` | 名字「Mia」 |
| 101 | 26 | 任务：Recovering the Crystal | 被抓偷窥 `85` | 前置「Victoria」、图片「Black」 |
| 102 | 26 | 任务：Recovering the Crystal | 地穴 · 白天 `129` | 图片「Black」 |
| 103 | 26 | 任务：Recovering the Crystal | Victoria · 剧情03 灵药 `148` | 名字「Potion」 |
| 104 | 26 | 任务：Recovering the Crystal | Victoria · 来访 `192` | 名字「Victoria」 |
| 105 | 26 | 任务：Recovering the Crystal | Victoria · 自慰1 `145` | 名字「Victoria」 |
| 106 | 26 | 任务：Recovering the Crystal | Victoria · 自慰2 `146` | 名字「Victoria」 |
| 107 | 26 | 任务：Recovering the Crystal | Victoria × 女儿 `291` | 名字「女儿」 |
| 108 | 26 | 任务：Recovering the Crystal | Victoria × 女儿（灵药） `309` | 名字「女儿」 |
| 109 | 26 | 任务：Recovering the Crystal | Caleah · 初次约会 `160` | 名字「Date」 |
| 110 | 26 | 任务：Recovering the Crystal | Frida · H 坏宠物 `166` | 名字「Frida」 |
| 111 | 26 | 任务：Recovering the Crystal | Frida · H 好宠物 `167` | 名字「Frida」 |
| 112 | 26 | 任务：Recovering the Crystal | Frida · H01A `165` | 名字「Frida」 |
| 113 | 26 | 任务：Recovering the Crystal | 龙 · 灵药 H2 `238` | 名字「Potion」 |
| 114 | 26 | 任务：Recovering the Crystal | Alice · 试衣间 灵药 `270` | 名字「Alice」 |
| 115 | 26 | 任务：Recovering the Crystal | Alice · 酒馆 H `267` | 名字「Alice」 |
| 116 | 26 | 任务：Recovering the Crystal | 女儿 · 去游泳 `293` | 名字「女儿」 |
| 117 | 26 | 任务：Recovering the Crystal | 女儿 · 去游泳（灵药） `345` | 名字「女儿」 |
| 118 | 26 | 任务：Recovering the Crystal | 女儿 · 床上1 `295` | 名字「女儿」 |
| 119 | 26 | 任务：Recovering the Crystal | 与女儿组队 `308` | 图片「Black」 |
| 120 | 26 | 任务：Recovering the Crystal | Liandra × 地精 `336` | 名字「Liandra」 |
| 121 | 26 | 任务：Recovering the Crystal | Liandra × 地精（灵药） `346` | 名字「Potion」 |
| 122 | 29 | 任务：The Crown of Sorcery | Erevi · 与主角 双人 `1249` | 名字「Erevi」、前置「Erevi」 |
| 123 | 29 | 任务：The Crown of Sorcery | Erevi · 床上2 `302` | 名字「Erevi」、前置「Erevi」 |
| 124 | 29 | 任务：The Crown of Sorcery | Erevi · 床上 H `1252` | 名字「Erevi」、前置「Erevi」 |
| 125 | 29 | 任务：The Crown of Sorcery | Erevi · 床上速战2 `301` | 名字「Erevi」 |
| 126 | 29 | 任务：The Crown of Sorcery | Erevi · 支配01 `18` | 名字「Erevi」 |
| 127 | 29 | 任务：The Crown of Sorcery | Erevi · 支配 H `168` | 名字「Erevi」 |
| 128 | 29 | 任务：The Crown of Sorcery | Erevi · 新婚夜 `1832` | 名字「Erevi」、前置「Erevi」 |
| 129 | 29 | 任务：The Crown of Sorcery | Erevi · 新婚夜 ED `1833` | 名字「Erevi」、前置「Erevi」 |
| 130 | 29 | 任务：The Crown of Sorcery | Erevi · 池塘 灵药 `1835` | 名字「Potion」、前置「Erevi」 |
| 131 | 29 | 任务：The Crown of Sorcery | Erevi · 绑在床上 H `1253` | 名字「Erevi」、前置「Erevi」 |
| 132 | 29 | 任务：The Crown of Sorcery | Erevi · 黑色礼服 `46` | 名字「Black」、前置「Erevi」 |
| 133 | 29 | 任务：The Crown of Sorcery | 地牢装置 · Erevi `1494` | 名字「Erevi」、前置「Alice」 |
| 134 | 30 | 任务：学徒 | 蝙蝠饲养者 · 沙发 H `530` | 名字「Breeder」、前置「Breeder」 |
| 135 | 30 | 任务：学徒 | 地牢01 · 解放BB `532` | 前置「Breeder」 |
| 136 | 30 | 任务：学徒 | 地牢04 · 解放BB `533` | 前置「Breeder」 |
| 137 | 30 | 任务：学徒 | 地牢 · 慰藉 `821` | 前置「Breeder」 |
| 138 | 32 | 任务：蝙蝠饲养者 | 离开地精洞 `338` | 名字「Cave」、前置「Liandra」 |
| 139 | 37 | 任务：孕妇装 | Mia · 林中相遇 `228` | 名字「Forest」、前置「Outfit」 |
| 140 | 37 | 任务：孕妇装 | Daiyu · 服装 BT `1637` | 名字「Outfit」、前置「Potion」 |
| 141 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Urakhand × Caleah `115` | 名字「Caleah」 |
| 142 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Urakhand × Caleah（回想） `127` | 名字「Caleah」 |
| 143 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · H02 `163` | 名字「Caleah」、前置「Caleah」 |
| 144 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · TF 变身 `2004` | 名字「Caleah」 |
| 145 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · 书库 H `917` | 名字「Caleah」、前置「Caleah」 |
| 146 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · 床上 `1489` | 名字「Caleah」、前置「Caleah」 |
| 147 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · 群体 上 `808` | 名字「Caleah」、前置「Alice」 |
| 148 | 46 | 任务：与 Beth 的约会 | Erevi · 床上 `121` | 名字「Erevi」、前置「Summon」 |
| 149 | 47 | 任务：与 Mia 的约会 | 女儿 · 巨魔 `1250` | 名字「女儿」、前置「Play」 |
| 150 | 47 | 任务：与 Mia 的约会 | 女儿 · 王子 `1254` | 名字「女儿」、前置「Play」 |
| 151 | 47 | 任务：与 Mia 的约会 | 女儿们玩耍 · 序 `1285` | 名字「Play」、前置「Erevi」 |
| 152 | 54 | 任务：增强生育力 | 龙 · 战后 `203` | 名字「Dragon」 |
| 153 | 54 | 任务：增强生育力 | 龙 · 灵药 H1 `237` | 名字「Potion」、前置「Dragon」 |
| 154 | 54 | 任务：增强生育力 | 龙 · 遭遇 `202` | 名字「Dragon」 |
| 155 | 62 | 任务：Waystone 任务 第1部分 | 归还传送石 `279` | 名字「Waystone」 |
| 156 | 64 | 任务：给面包师的面粉 | Rosy · 强制口交 `323` | 名字「Rosy」 |
| 157 | 64 | 任务：给面包师的面粉 | Rosy · 面包店02 `333` | 名字「Rosy」、前置「Rosy」 |
| 158 | 64 | 任务：给面包师的面粉 | Rosy · 面包店03 `690` | 名字「Rosy」、前置「Rosy」 |
| 159 | 69 | 任务：叫接生婆 | Hilde · 帐篷2 `365` | 名字「Hilde」、前置「Hilde」 |
| 160 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 `366` | 名字「Hilde」 |
| 161 | 69 | 任务：叫接生婆 | Hilde · 帐篷 `360` | 名字「Hilde」、前置「Hilde」 |
| 162 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 主线 `1414` | 名字「Hilde」、前置「Hilde」 |
| 163 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 后门 `1415` | 名字「Hilde」、前置「Hilde」 |
| 164 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 正常位 `1416` | 名字「Hilde」、前置「Hilde」 |
| 165 | 69 | 任务：叫接生婆 | Hilde · 帐篷3B `370` | 名字「Hilde」 |
| 166 | 69 | 任务：叫接生婆 | Hilde · 新婚夜 `357` | 名字「Hilde」 |
| 167 | 69 | 任务：叫接生婆 | Hilde · 沐浴 `359` | 名字「Hilde」、前置「Hilde」 |
| 168 | 69 | 任务：叫接生婆 | Hilde · 温泉 `1418` | 名字「Hilde」、前置「Hilde」 |
| 169 | 69 | 任务：叫接生婆 | Freyja宴 · Hilde 未中 `1486` | 名字「Hilde」、前置「Hilde」 |
| 170 | 69 | 任务：叫接生婆 | Freyja宴 · Hilde 骑乘 `1483` | 名字「Riding」、前置「Hilde」 |
| 171 | 75 | 任务：与 Maghda 的亲密时光 | Jenny · 奶酪 `1270` | 名字「Jenny」、前置「Jenny」 |
| 172 | 75 | 任务：与 Maghda 的亲密时光 | Jenny · 奶酪 XL `1269` | 名字「Jenny」、前置「Jenny」 |
| 173 | 75 | 任务：与 Maghda 的亲密时光 | Jenny · 手交 `732` | 名字「Jenny」、前置「Jenny」 |
| 174 | 83 | 任务：叛乱的部落 | Sequoia · H1 `476` | 名字「Sequoia」、前置「Sequoia」 |
| 175 | 83 | 任务：叛乱的部落 | Sequoia · H2 `477` | 名字「Sequoia」、前置「Sequoia」 |
| 176 | 88 | 任务：男人窝 | 地牢装置 · BB `1497` | 名字「地牢」、前置「Breeder」 |
| 177 | 88 | 任务：男人窝 | 地牢装置 · ED `1498` | 名字「地牢」、前置「Erevi」 |
| 178 | 92 | 任务：织网大师 | 蜘蛛娘 · 化人 `519` | 名字「Spider」、前置「Venomina」 |
| 179 | 92 | 任务：织网大师 | 蜘蛛洞 · 剧情3 `521` | 名字「Spider」、前置「Venomina」 |
| 180 | 92 | 任务：织网大师 | 蜘蛛洞 · 剧情4 `536` | 名字「Spider」、前置「Venomina」 |
| 181 | 92 | 任务：织网大师 | 蜘蛛洞 · 剧情5 `535` | 名字「Spider」、前置「Venomina」 |
| 182 | 92 | 任务：织网大师 | 吸血鬼受害者 Reanna 3 `669` | 名字「受害者」、前置「Black」 |
| 183 | 93 | 任务：猎巫人 | 墓园 · 夜晚 `130` | 名字「Cemetery」 |
| 184 | 93 | 任务：猎巫人 | Oksana · TF 变身 `2002` | 名字「Oksana」、前置「Oksana」 |
| 185 | 93 | 任务：猎巫人 | Oksana · 后门祭坛 H `1056` | 名字「Oksana」、前置「Heal」 |
| 186 | 93 | 任务：猎巫人 | Oksana · 地穴 H `687` | 名字「Oksana」、前置「Potion」 |
| 187 | 93 | 任务：猎巫人 | Oksana · 神殿后门 H `1052` | 名字「Temple」、前置「Oksana」 |
| 188 | 93 | 任务：猎巫人 | Oksana · 群体 上 `1070` | 名字「Oksana」、前置「Alice」 |
| 189 | 94 | 任务：淑女的连衣裙 | Zsofia · 卧室来访 `677` | 名字「Zsofia」、前置「Zsofia」 |
| 190 | 94 | 任务：淑女的连衣裙 | Zsofia · 墓园 H `546` | 名字「Cemetery」、前置「Zsofia」 |
| 191 | 95 | 任务：寻找旅店老板 | Oksana · 沐浴贿赂Oliver `651` | 名字「Oksana」、前置「Oliver」 |
| 192 | 96 | 任务：进一步调查 | 职责召唤 `1804` | 图片「Castle」 |
| 193 | 97 | 任务：净化者 | Adaobi · 卧室来访 `678` | 名字「Adaobi」、前置「Adaobi」 |
| 194 | 97 | 任务：净化者 | Adaobi · 礼拜堂 H `671` | 名字「Adaobi」、前置「Potion」 |
| 195 | 97 | 任务：净化者 | Reanna · 军械库口交 `686` | 名字「Reanna」 |
| 196 | 97 | 任务：净化者 | Reanna · 卧室 H `674` | 名字「Reanna」、前置「Outfit」 |
| 197 | 97 | 任务：净化者 | Reanna · 小巷2 `1646` | 名字「Reanna」、前置「Potion」 |
| 198 | 97 | 任务：净化者 | Reanna · 小巷 `1645` | 名字「Reanna」 |
| 199 | 97 | 任务：净化者 | 对峙灰港杀手 `1784` | 名字「Killer」 |
| 200 | 108 | 任务：一笔贷款？ | 酒馆 · 掷骰 `727` | 名字「Play」、前置「Dice」 |
| 201 | 111 | 任务：遇险的母子 | 女儿 · 床上2 `297` | 名字「女儿」、前置「Room」 |
| 202 | 111 | 任务：遇险的母子 | Victoria · 白丝 怀孕（灵药） `656` | 名字「Victoria」 |
| 203 | 111 | 任务：遇险的母子 | Victoria · 红色内衣 `415` | 名字「Victoria」 |
| 204 | 111 | 任务：遇险的母子 | Victoria · 红色内衣 怀孕（灵药） `654` | 名字「Victoria」 |
| 205 | 111 | 任务：遇险的母子 | 探望 Victoria（产后） `416` | 名字「Victoria」 |
| 206 | 111 | 任务：遇险的母子 | Oksana · 沐浴 `684` | 名字「Oksana」 |
| 207 | 115 | 任务：家族生意 | Luthien · 不在场证明 `988` | 名字「Luthien」、前置「Liandra」 |
| 208 | 115 | 任务：家族生意 | Luthien · 小屋椅子上 H `983` | 名字「Luthien」、前置「Luthien」 |
| 209 | 115 | 任务：家族生意 | Luthien · 桌上 H `997` | 名字「Luthien」、前置「Luthien」 |
| 210 | 115 | 任务：家族生意 | Luthien · 液体愉悦 `982` | 名字「Delight」 |
| 211 | 115 | 任务：家族生意 | Luthien · 胸部按摩 `998` | 名字「Luthien」 |
| 212 | 125 | 任务：家族纽带 | Julia · 床上 `1080` | 名字「Julia」、前置「Julia」 |
| 213 | 125 | 任务：家族纽带 | Julia · 狐狸 H `1262` | 名字「Julia」、前置「Julia」 |
| 214 | 125 | 任务：家族纽带 | Julia · 第一次游泳 `1063` | 名字「Julia」 |
| 215 | 125 | 任务：家族纽带 | Julia · 第三次游泳 `1065` | 名字「Julia」 |
| 216 | 125 | 任务：家族纽带 | Julia · 第二次游泳 `1064` | 名字「Julia」 |
| 217 | 125 | 任务：家族纽带 | Julia · 谷仓 H `1264` | 名字「Julia」、前置「Julia」 |
| 218 | 125 | 任务：家族纽带 | Julia · 谷仓婚礼 `1069` | 名字「Julia」、前置「Julia」 |
| 219 | 125 | 任务：家族纽带 | Annabelle×Julia · H `1263` | 名字「Julia」、前置「Julia」 |
| 220 | 134 | 任务：神秘失踪 | Obeah · 地上 H `1157` | 名字「Obeah」、前置「Obeah」 |
| 221 | 134 | 任务：神秘失踪 | Obeah · 被俘 下 `1160` | 名字「Obeah」 |
| 222 | 134 | 任务：神秘失踪 | Obeah · 长椅 H `1154` | 名字「Obeah」、前置「Obeah」 |
| 223 | 138 | 任务：香水 | 送莲花提取物 `1275` | 名字「Extract」 |
| 224 | 151 | 任务145：成长！ | Annabelle · 挤奶 `1267` | 名字「Annabelle」、前置「Annabelle」 |
| 225 | 151 | 任务145：成长！ | Annabelle · 未中出 `1266` | 名字「Annabelle」、前置「Annabelle」 |
| 226 | 151 | 任务145：成长！ | Annabelle · 谷仓 H `1265` | 名字「Annabelle」、前置「Annabelle」 |
| 227 | 151 | 任务145：成长！ | Annabelle · 谷仓口交 `1412` | 名字「Annabelle」、前置「Annabelle」 |
| 228 | 151 | 任务145：成长！ | Julia · 挤奶 `1268` | 名字「Julia」、前置「Annabelle」 |
| 229 | 151 | 任务145：成长！ | Julia · 谷仓口交 `1411` | 名字「Julia」、前置「Annabelle」 |
| 230 | 159 | 任务156：狩猎 | Hilde · 帐篷3A `369` | 名字「Hilde」、前置「Birgitte」 |
| 231 | 159 | 任务156：狩猎 | Hilde · 帐篷3C `379` | 名字「Hilde」、前置「Birgitte」 |
| 232 | 159 | 任务156：狩猎 | 狩猎小屋 · H（大场景） `1417` | 名字「Hunting」、前置「Frida」 |
| 233 | 159 | 任务156：狩猎 | Birgitte · 小屋2 内衣 `1420` | 名字「Lingerie」、前置「Birgitte」 |
| 234 | 159 | 任务156：狩猎 | Birgitte · 小屋2 裸体 `1419` | 名字「Birgitte」、前置「Birgitte」 |
| 235 | 159 | 任务156：狩猎 | Birgitte · 椅子上 `1481` | 名字「Birgitte」、前置「Potions」 |
| 236 | 159 | 任务156：狩猎 | Freyja宴 · Birgitte 未中 `1487` | 名字「Birgitte」、前置「Birgitte」 |
| 237 | 159 | 任务156：狩猎 | Freyja宴 · Birgitte 骑乘 `1484` | 名字「Riding」、前置「Birgitte」 |
| 238 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · DT `1643` | 名字「Daiyu」、前置「Daiyu」 |
| 239 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台1 `1634` | 名字「Daiyu」、前置「Potion」 |
| 240 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台2 `1635` | 名字「Daiyu」、前置「Potion」 |
| 241 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台1 SP `1641` | 名字「Daiyu」、前置「Potion」 |
| 242 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台2 SP `1642` | 名字「Daiyu」、前置「Daiyu」 |
| 243 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 服装 `1636` | 名字「Outfit」、前置「Daiyu」 |
| 244 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 清晨 `1638` | 名字「Daiyu」、前置「Daiyu」 |
| 245 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 脱衣 `1782` | 名字「Daiyu」、前置「Daiyu」 |
| 246 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 自慰 `1639` | 名字「Daiyu」、前置「Daiyu」 |
| 247 | 170 | 任务167：被绑架了！ | ED · 湿身少女 `1644` | 名字「Maiden」、前置「Potions」 |
| 248 | 170 | 任务167：被绑架了！ | ED · 脱衣 `1783` | 图片「Maiden」 |
| 249 | 175 | 任务171：爱丽丝梦游仙境 | Naamah · H1 `1495` | 名字「Naamah」、前置「Naamah」 |
| 250 | 175 | 任务171：爱丽丝梦游仙境 | Naamah · H2 `1496` | 名字「Naamah」、前置「Naamah」 |
| 251 | 175 | 任务171：爱丽丝梦游仙境 | Naamah · H3 `1836` | 名字「Naamah」、前置「Naamah」 |
| 252 | 179 | 任务176：热门八卦 | Vix · 火山口1 `1632` | 名字「Vix」、前置「Vixenatrix」 |
| 253 | 179 | 任务176：热门八卦 | Vix · 火山口2 `1633` | 名字「Vix」、前置「Vixenatrix」 |
| 254 | 181 | 任务178：偷巢者！ | Tabufa · 卧室 `1631` | 名字「Tabufa」、前置「Tabufa」 |
| 255 | 181 | 任务178：偷巢者！ | Tabufa · 口交 `1500` | 名字「Tabufa」、前置「Tabufa」 |
| 256 | 181 | 任务178：偷巢者！ | Tabufa · 王座 `1499` | 名字「Tabufa」、前置「Tabufa」 |
| 257 | 188 | 任务185：承诺 | Erevi · 床上速战 `44` | 名字「Erevi」 |
| 258 | 188 | 任务185：承诺 | Erevi · 红色内衣（灵药） `652` | 名字「Potion」 |
| 259 | 188 | 任务185：承诺 | Victoria · 剧情02 灵药 `147` | 名字「Potion」 |
| 260 | 188 | 任务185：承诺 | Victoria · 黑色内衣 怀孕（灵药） `655` | 名字「Victoria」 |
| 261 | 188 | 任务185：承诺 | Josephine · 卧室 `1650` | 名字「Bedroom」、前置「Potion」 |
| 262 | 188 | 任务185：承诺 | Yvette · 新婚夜（大场景） `1657` | 名字「Wedding」、前置「Potion」 |
| 263 | 188 | 任务185：承诺 | Cathrine · 卧室4 `1659` | 名字「Bedroom」、前置「Potions」 |
| 264 | 188 | 任务185：承诺 | 同床 `1803` | 图片「Wedding」 |
| 265 | 190 | 任务187：开膛手 | Mia · 床上 H1 `232` | 名字「Mia」 |
| 266 | 190 | 任务187：开膛手 | Mia · 床上 H1（灵药） `919` | 名字「Potion」 |
| 267 | 190 | 任务187：开膛手 | Jenny · 初次怀孕 `742` | 名字「Jenny」 |
| 268 | 190 | 任务187：开膛手 | Jenny · 手交（无Tom） `750` | 名字「Jenny」 |
| 269 | 190 | 任务187：开膛手 | Tom · 第一次输 下 `754` | 名字「Tom」 |
| 270 | 190 | 任务187：开膛手 | Tom · 第三次输 下 `756` | 名字「Tom」 |
| 271 | 190 | 任务187：开膛手 | Tom · 第二次输 下 `755` | 名字「Tom」 |
| 272 | 191 | 任务188：锦标赛 | Yvette · PG5 `1821` | 名字「Yvette」、前置「Potion」 |
| 273 | 191 | 任务188：锦标赛 | Yvette · 假做 H `1654` | 名字「Yvette」、前置「Yvette」 |
| 274 | 191 | 任务188：锦标赛 | Yvette · 泳池 `1824` | 名字「Yvette」、前置「Yvette」 |
| 275 | 191 | 任务188：锦标赛 | Yvette · 泳池花园 H `1805` | 名字「Yvette」、前置「Yvette」 |
| 276 | 191 | 任务188：锦标赛 | Yvette · 自慰1 `1647` | 名字「Yvette」、前置「Yvette」 |
| 277 | 191 | 任务188：锦标赛 | Yvette · 自慰2 `1648` | 名字「Yvette」、前置「Yvette」 |
| 278 | 191 | 任务188：锦标赛 | Yvette · 调教 上 `1652` | 名字「Yvette」、前置「Yvette」 |
| 279 | 191 | 任务188：锦标赛 | Yvette · 调教 口交 `1653` | 名字「Yvette」、前置「Yvette」 |
| 280 | 196 | 任务193：中暑 | Josephine · 卧室 MM `1651` | 名字「Josephine」 |
| 281 | 196 | 任务193：中暑 | Josephine · 厨房 `1656` | 名字「Josephine」、前置「Wedding」 |
| 282 | 196 | 任务193：中暑 | Josephine · 泳池 `1649` | 名字「Josephine」、前置「Josephine」 |
| 283 | 196 | 任务193：中暑 | Josephine · 王座 `1660` | 名字「Josephine」、前置「Josephine」 |
| 284 | 197 | 任务194：Cathrine 修女 | Cathrine · 卧室3 `1658` | 名字「Bedroom」、前置「Cathrine」 |
| 285 | 197 | 任务194：Cathrine 修女 | Cathrine · 卧室5 `1822` | 名字「Bedroom」、前置「Cathrine」 |
| 286 | 197 | 任务194：Cathrine 修女 | Cathrine · 床上 `1825` | 名字「Cathrine」、前置「Cathrine」 |
| 287 | 197 | 任务194：Cathrine 修女 | Cathrine · 手交 `1655` | 名字「Cathrine」、前置「Cathrine」 |
| 288 | 197 | 任务194：Cathrine 修女 | Cathrine · 祭坛 PG `1827` | 名字「Cathrine」、前置「Phallus」 |
| 289 | 197 | 任务194：Cathrine 修女 | Cathrine · 祭坛 序 `1826` | 名字「Cathrine」、前置「Cathrine」 |
| 290 | 197 | 任务194：Cathrine 修女 | Cathrine · 祭坛 无PG `1828` | 名字「Cathrine」、前置「Cathrine」 |
| 291 | 198 | 任务195：神秘陌生人 | Baron · 登场 `1794` | 名字「Baron」 |
| 292 | 198 | 任务195：神秘陌生人 | Baron · 训斥 `1801` | 名字「Baron」 |
| 293 | 205 | 任务201：意志之战 | 水蛭袭击 `157` | 名字「Attack」 |
| 294 | 205 | 任务201：意志之战 | 骑士袭击 `496` | 名字「Attack」、前置「Shakala」 |
| 295 | 212 | 任务208：Enchanted Forest | 精灵 · 之后 `1831` | 名字「精灵」 |
| 296 | 212 | 任务208：Enchanted Forest | 精灵 · 初次 `1830` | 名字「精灵」 |
| 297 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满1 H `1241` | 名字「蝙蝠洞」、前置「Breeder」 |
| 298 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满2 H `1245` | 名字「蝙蝠洞」、前置「Breeder」 |
| 299 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满1 NP H `1242` | 名字「蝙蝠洞」、前置「Breeder」 |
| 300 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满2 NP H `1246` | 名字「蝙蝠洞」、前置「Breeder」 |
| 301 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小1 H `1243` | 名字「蝙蝠洞」、前置「Breeder」 |
| 302 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小2 H `1247` | 名字「蝙蝠洞」、前置「Breeder」 |
| 303 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小1 NP H `1244` | 名字「蝙蝠洞」、前置「Breeder」 |
| 304 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小2 NP H `1248` | 名字「蝙蝠洞」、前置「Breeder」 |
| 305 | — | （未定位） | 解锁 · 小恶魔口交 `847` | — |
| 306 | — | （未定位） | 初次游泳（大场景） `1795` | — |
