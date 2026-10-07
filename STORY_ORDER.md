# 剧情顺序（storyOrder）

依据游戏自带中文攻略的任务顺序（219 个章节）给场景定位，
由 `tools/story_order.py` 生成。

章节内按人物组、子线名、名字编号排序；定位不到的排在最后，可在 `params/storyOverrides.json` 里手工订正。

| 顺序 | 剧情章节 | 章节标题 | 场景 | 定位依据 |
|---|---|---|---|---|
| 1 | 2 | 任务：找到偷猎者 | Map090 · 事件29 `m90:29` | 地点「哥布林」 |
| 2 | 3 | 任务：与所有村民交谈 | Alice · TF 变身 `2001` | 名字「Alice」、前置「Alice」 |
| 3 | 3 | 任务：与所有村民交谈 | Alice · 书库 H `262` | 名字「Alice」、前置「Alice」 |
| 4 | 3 | 任务：与所有村民交谈 | Alice · 厨房 H `261` | 名字「Alice」、前置「Alice」 |
| 5 | 3 | 任务：与所有村民交谈 | Alice · 她的房间 `256` | 名字「Alice」、前置「Alice」 |
| 6 | 3 | 任务：与所有村民交谈 | Alice · 房间 灵药 `268` | 名字「Alice」 |
| 7 | 3 | 任务：与所有村民交谈 | Alice · 神龛 H `260` | 名字「Alice」、前置「Alice」 |
| 8 | 3 | 任务：与所有村民交谈 | Alice · 约会 `266` | 名字「Alice」 |
| 9 | 3 | 任务：与所有村民交谈 | Alice · 群体 上 `807` | 名字「Alice」、前置「Alice」 |
| 10 | 3 | 任务：与所有村民交谈 | Alice · 试衣间 `255` | 名字「Alice」、前置「Alice」 |
| 11 | 3 | 任务：与所有村民交谈 | Alice · 酿酒 H `1261` | 名字「Alice」、前置「Alice」 |
| 12 | 3 | 任务：与所有村民交谈 | Alice · 锁链1 `1492` | 名字「Alice」、前置「Alice」 |
| 13 | 3 | 任务：与所有村民交谈 | Alice · 锁链2 `1493` | 名字「Alice」、前置「Alice」 |
| 14 | 3 | 任务：与所有村民交谈 | Alice × Johan 桌边 `264` | 名字「Alice」、前置「Alice」 |
| 15 | 3 | 任务：与所有村民交谈 | 女儿 · 伏击之后 `1781` | 名字「女儿」 |
| 16 | 3 | 任务：与所有村民交谈 | 女儿 · 床上3 `298` | 名字「女儿」 |
| 17 | 3 | 任务：与所有村民交谈 | Gwynneth · 宅邸2 H `459` | 名字「Gwynneth」、前置「Gwynneth」 |
| 18 | 3 | 任务：与所有村民交谈 | Gwynneth · 家中（灵药） `1259` | 名字「Gwynneth」、前置「Gwynneth」 |
| 19 | 3 | 任务：与所有村民交谈 | Gwynneth · 床上 H `1258` | 名字「Gwynneth」、前置「Gwynneth」 |
| 20 | 3 | 任务：与所有村民交谈 | Victoria×Gwynneth · H（大场景） `1257` | 名字「Gwynneth」、前置「Gwynneth」 |
| 21 | 3 | 任务：与所有村民交谈 | Beth · 床上 `1490` | 名字「Beth」、前置「Beth」 |
| 22 | 3 | 任务：与所有村民交谈 | Beth · 求欢2 `1557` | 名字「Beth」、前置「Beth」 |
| 23 | 3 | 任务：与所有村民交谈 | Beth · 求欢1（大场景） `1556` | 名字「Beth」、前置「Beth」 |
| 24 | 3 | 任务：与所有村民交谈 | Beth · 马厩 N6 `1488` | 名字「Beth」、前置「Beth」 |
| 25 | 3 | 任务：与所有村民交谈 | 跳跃的驴子 · 事件7 `m5:7` | 地点「Alice」 |
| 26 | 3 | 任务：与所有村民交谈 | 跳跃的驴子 · 事件26 `m5:26` | 地点「旅店」 |
| 27 | 3 | 任务：与所有村民交谈 | 跳跃的驴子 · 事件31 `m5:31` | 地点「旅店」 |
| 28 | 3 | 任务：与所有村民交谈 | Map009 · 事件19 `m9:19` | 地点「Gabriel」 |
| 29 | 3 | 任务：与所有村民交谈 | Map009 · 事件45 `m9:45` | 地点「Gwynneth」 |
| 30 | 3 | 任务：与所有村民交谈 | Map148 · 事件6 `m148:6` | 地点「Gwynneth」 |
| 31 | 3 | 任务：与所有村民交谈 | Map165 · 事件4 `m165:4` | 地点「Beth」 |
| 32 | 4 | 任务：失踪的货物 | Maghda · 怀孕 H1 `395` | 名字「Maghda」、前置「Maghda」 |
| 33 | 4 | 任务：失踪的货物 | Maghda · 怀孕 H2 `397` | 名字「Maghda」、前置「Maghda」 |
| 34 | 4 | 任务：失踪的货物 | Maghda · 怀孕 H3 `400` | 名字「Maghda」 |
| 35 | 4 | 任务：失踪的货物 | Maghda · 洞中 H `1255` | 名字「Maghda」、前置「Maghda」 |
| 36 | 4 | 任务：失踪的货物 | Maghda · 洞外 H `1256` | 名字「Maghda」、前置「Dolf」 |
| 37 | 4 | 任务：失踪的货物 | Maghda × Dolf 02 `40` | 名字「Dolf」 |
| 38 | 4 | 任务：失踪的货物 | Maghda × Dolf 03 `41` | 名字「Dolf」、前置「Maghda」 |
| 39 | 4 | 任务：失踪的货物 | Maghda × Dolf 04 `386` | 名字「Dolf」 |
| 40 | 4 | 任务：失踪的货物 | Maghda × Dolf 05 `1356` | 名字「Dolf」、前置「Dolf」 |
| 41 | 4 | 任务：失踪的货物 | Erevi · 黑色礼服（灵药） `653` | 名字「Potion」 |
| 42 | 4 | 任务：失踪的货物 | Erevi × 女儿 `304` | 名字「女儿」、前置「Potion」 |
| 43 | 4 | 任务：失踪的货物 | Liandra · H2 灵药 `347` | 名字「Potion」 |
| 44 | 4 | 任务：失踪的货物 | 观看地精女儿 阶段1 `482` | 图片「Goblin」 |
| 45 | 4 | 任务：失踪的货物 | 观看地精女儿 阶段2 `483` | 图片「Goblin」 |
| 46 | 4 | 任务：失踪的货物 | 地精女儿 · 剧情01 `487` | 图片「Goblin」 |
| 47 | 4 | 任务：失踪的货物 | 地精女儿 · 剧情02 `488` | 前置「Goblin」、图片「Goblin」 |
| 48 | 4 | 任务：失踪的货物 | 地精女儿 · 剧情03 `489` | 前置「Goblin」、图片「Goblin」 |
| 49 | 4 | 任务：失踪的货物 | Shakala · 林中 H `503` | 名字「Forest」 |
| 50 | 4 | 任务：失踪的货物 | 地穴 H（灵药·大场景） `685` | 名字「Potion」 |
| 51 | 4 | 任务：失踪的货物 | 使魔 · 变身 `816` | 图片「Forest」 |
| 52 | 4 | 任务：失踪的货物 | Map009 · 事件18 `m9:18` | 地点「Forest」 |
| 53 | 4 | 任务：失踪的货物 | 北方森林 · 事件3 `m13:3` | 地点「Forest」 |
| 54 | 4 | 任务：失踪的货物 | 北方森林 · 事件15 `m13:15` | 地点「Forest」 |
| 55 | 4 | 任务：失踪的货物 | 北方森林 · 事件28 `m13:28` | 地点「Forest」 |
| 56 | 4 | 任务：失踪的货物 | 北方森林 · 事件32 `m13:32` | 地点「Forest」 |
| 57 | 4 | 任务：失踪的货物 | Map040 · 事件7 `m40:7` | 地点「Dolf」、调用场景的章节 4 |
| 58 | 4 | 任务：失踪的货物 | Map153 · 事件67 `m153:67` | 地点「Goblin」 |
| 59 | 4 | 任务：失踪的货物 | Map154 · 事件14 `m154:14` | 地点「Goblin」 |
| 60 | 4 | 任务：失踪的货物 | Map187 · 事件59 `m187:59` | 地点「Forest」 |
| 61 | 5 | 任务：哥布林耳朵 | Shakala · GD H01 `497` | 名字「Shakala」、前置「Goblin」 |
| 62 | 5 | 任务：哥布林耳朵 | Shakala · 事件01 `15` | 名字「Shakala」 |
| 63 | 5 | 任务：哥布林耳朵 | Shakala · 事件02 `16` | 名字「Shakala」、前置「Shakala」 |
| 64 | 5 | 任务：哥布林耳朵 | Shakala · 事件03 `17` | 名字「Shakala」 |
| 65 | 5 | 任务：哥布林耳朵 | Shakala · 婚礼 上 `67` | 名字「Shakala」 |
| 66 | 5 | 任务：哥布林耳朵 | Shakala · 婚礼双人 `504` | 名字「Shakala」 |
| 67 | 5 | 任务：哥布林耳朵 | Shakala · 桌上 H `1151` | 名字「Shakala」、前置「Shakala」 |
| 68 | 5 | 任务：哥布林耳朵 | 沙卡拉斯村 · 事件23 `m32:23` | 地点「哥布林」、调用场景的章节 5 |
| 69 | 6 | 任务：与Alice的约会 | 怪木林 · 事件216 `m1:216` | 地点「Weirdwood」 |
| 70 | 7 | 任务：望远镜 | Maghda × Dolf 01 `39` | 名字「Dolf」 |
| 71 | 7 | 任务：望远镜 | Map014 · 事件2 `m14:2` | 地点「House」 |
| 72 | 10 | 任务：Witch Trouble | 神殿 · 入会仪式 `125` | 名字「Temple」 |
| 73 | 10 | 任务：Witch Trouble | Caleah × Ziva H（大场景） `214` | 名字「Ziva」、前置「Potion」 |
| 74 | 10 | 任务：Witch Trouble | 蜘蛛娘 · 杂交 H `518` | 名字「Spider」、前置「Spider」 |
| 75 | 10 | 任务：Witch Trouble | 蜘蛛娘 · 阶段0 `514` | 名字「Spider」 |
| 76 | 10 | 任务：Witch Trouble | 蜘蛛娘 · 阶段1 `515` | 名字「Spider」 |
| 77 | 10 | 任务：Witch Trouble | 被蜘蛛娘抓住 `520` | 名字「Spider」 |
| 78 | 10 | 任务：Witch Trouble | 蜘蛛洞 · 剧情3B `526` | 名字「Spider」、前置「Spider」 |
| 79 | 10 | 任务：Witch Trouble | Oksana · 神殿 H（灵药） `683` | 名字「Temple」 |
| 80 | 10 | 任务：Witch Trouble | Ziva · TF 变身 `2003` | 名字「Ziva」、前置「Ziva」 |
| 81 | 10 | 任务：Witch Trouble | Ziva · 群体 上 `806` | 名字「Ziva」、前置「Alice」 |
| 82 | 10 | 任务：Witch Trouble | 女儿 · 地牢玩具 `1251` | 名字「女儿」、前置「Nergal」 |
| 83 | 10 | 任务：Witch Trouble | 告诉Gabriel关于Beth `1477` | 名字「Beth」、前置「Temple」 |
| 84 | 10 | 任务：Witch Trouble | Qetesh · 喷泉 `1491` | 名字「Qetesh」、前置「Qetesh」 |
| 85 | 10 | 任务：Witch Trouble | Qetesh · 宫殿1 `1837` | 名字「Qetesh」、前置「Qetesh」 |
| 86 | 10 | 任务：Witch Trouble | Qetesh · 宫殿2 `1838` | 名字「Qetesh」、前置「Qetesh」 |
| 87 | 10 | 任务：Witch Trouble | Qetesh · 床上 `1829` | 名字「Qetesh」、前置「Qetesh」 |
| 88 | 10 | 任务：Witch Trouble | Map015 · 事件2 `m15:2` | 地点「Temple」 |
| 89 | 10 | 任务：Witch Trouble | Map015 · 事件8 `m15:8` | 地点「Temple」 |
| 90 | 10 | 任务：Witch Trouble | Map061 · 事件61 `m61:61` | 地点「Temple」、调用场景的章节 10 |
| 91 | 10 | 任务：Witch Trouble | Map061 · 事件75 `m61:75` | 地点「Temple」 |
| 92 | 10 | 任务：Witch Trouble | Map092 · 事件3 `m92:3` | 地点「Spider」 |
| 93 | 10 | 任务：Witch Trouble | Map095 · 事件87 `m95:87` | 地点「Ziva」 |
| 94 | 10 | 任务：Witch Trouble | Map192 · 事件10 `m192:10` | 地点「Qetesh」、调用场景的章节 10 |
| 95 | 11 | 任务：Sacred Water | Liandra · H2 `340` | 名字「Liandra」 |
| 96 | 11 | 任务：Sacred Water | Liandra · 井边 H `1166` | 名字「Liandra」 |
| 97 | 11 | 任务：Sacred Water | Liandra · 井边口交 `1165` | 名字「Liandra」 |
| 98 | 11 | 任务：Sacred Water | Liandra · 井边脱衣 `1164` | 名字「Liandra」 |
| 99 | 11 | 任务：Sacred Water | Liandra · 卧室 H `990` | 名字「Liandra」、前置「Liandra」 |
| 100 | 11 | 任务：Sacred Water | Liandra · 床上裸体 H `989` | 名字「Liandra」、前置「Liandra」 |
| 101 | 11 | 任务：Sacred Water | Liandra · 怀孕 H `341` | 名字「Liandra」 |
| 102 | 11 | 任务：Sacred Water | Liandra · 花园 `978` | 名字「Liandra」、前置「Liandra」 |
| 103 | 11 | 任务：Sacred Water | Lu × Li 三人行 `1087` | 前置「Liandra」 |
| 104 | 11 | 任务：Sacred Water | Caleah · 酿酒 H `1260` | 名字「Wine」、前置「Alice」 |
| 105 | 11 | 任务：Sacred Water | 拜访酿酒姑娘们 `1394` | 名字「Wine」、前置「Alice」 |
| 106 | 11 | 任务：Sacred Water | 魔法之井 · 事件2 `m8:2` | 地点「Well」 |
| 107 | 11 | 任务：Sacred Water | 魔法之井 · 事件3 `m8:3` | 地点「Forest」、调用场景的章节 11 |
| 108 | 11 | 任务：Sacred Water | Map018 · 事件4 `m18:4` | 地点「的住处」 |
| 109 | 12 | 任务：租房 | Victoria · 剧情01 `103` | 名字「Victoria」、前置「Victoria」 |
| 110 | 12 | 任务：租房 | Victoria · 剧情02 `106` | 名字「Victoria」、前置「Potion」 |
| 111 | 12 | 任务：租房 | Victoria · 剧情03 `107` | 名字「Victoria」、前置「Potion」 |
| 112 | 12 | 任务：租房 | Victoria · 怀孕 H01 `139` | 名字「Victoria」、前置「Victoria」 |
| 113 | 12 | 任务：租房 | Victoria · 蓝色服装 `1834` | 名字「Victoria」、前置「Victoria」 |
| 114 | 12 | 任务：租房 | Victoria · 裸体 `452` | 名字「Victoria」、前置「Victoria」 |
| 115 | 18 | 任务：The Temple of Qetesh | Grug · 受伤 `117` | 名字「Grug」 |
| 116 | 18 | 任务：The Temple of Qetesh | Oksana · 神殿卧室3 H `1051` | 名字「Temple」、前置「Heal」 |
| 117 | 22 | 任务：哥布林炼金术 | Erevi · 灵药受孕 `169` | 名字「Spirit」 |
| 118 | 22 | 任务：哥布林炼金术 | ED · 课程 `1823` | 前置「Potions」 |
| 119 | 25 | 任务：拯救小狗！ | Frida · 帐篷口交（灵药） `378` | 名字「Potion」 |
| 120 | 25 | 任务：拯救小狗！ | Frida · 床上 H（怀孕） `88` | 名字「Frida」 |
| 121 | 25 | 任务：拯救小狗！ | Frida · 床上 H（未孕） `87` | 名字「Frida」、前置「Frida」 |
| 122 | 25 | 任务：拯救小狗！ | Frida · 调情 `13` | 名字「Frida」、前置「Frida」 |
| 123 | 25 | 任务：拯救小狗！ | Freyja宴 · Frida 未中 `1485` | 名字「Frida」、前置「Frida」 |
| 124 | 25 | 任务：拯救小狗！ | Freyja宴 · Frida 骑乘 `1482` | 名字「Frida」、前置「Frida」 |
| 125 | 26 | 任务：Recovering the Crystal | Ziva · 剧情01 `10` | 名字「Ziva」 |
| 126 | 26 | 任务：Recovering the Crystal | Mia · 与祖母对峙 `235` | 名字「Mia」 |
| 127 | 26 | 任务：Recovering the Crystal | Mia · 口交 `66` | 名字「Mia」 |
| 128 | 26 | 任务：Recovering the Crystal | Mia · 接吻 `63` | 名字「Mia」 |
| 129 | 26 | 任务：Recovering the Crystal | Mia · 私处 `65` | 名字「Mia」 |
| 130 | 26 | 任务：Recovering the Crystal | Mia · 胸部 `64` | 名字「Mia」 |
| 131 | 26 | 任务：Recovering the Crystal | 被抓偷窥 `85` | 前置「Victoria」、图片「Black」 |
| 132 | 26 | 任务：Recovering the Crystal | 地穴 · 白天 `129` | 图片「Black」 |
| 133 | 26 | 任务：Recovering the Crystal | Victoria · 剧情03 灵药 `148` | 名字「Potion」 |
| 134 | 26 | 任务：Recovering the Crystal | Victoria · 来访 `192` | 名字「Victoria」 |
| 135 | 26 | 任务：Recovering the Crystal | Victoria · 自慰1 `145` | 名字「Victoria」 |
| 136 | 26 | 任务：Recovering the Crystal | Victoria · 自慰2 `146` | 名字「Victoria」 |
| 137 | 26 | 任务：Recovering the Crystal | Victoria × 女儿 `291` | 名字「女儿」 |
| 138 | 26 | 任务：Recovering the Crystal | Victoria × 女儿（灵药） `309` | 名字「女儿」 |
| 139 | 26 | 任务：Recovering the Crystal | Caleah · 初次约会 `160` | 名字「Date」 |
| 140 | 26 | 任务：Recovering the Crystal | Frida · H 坏宠物 `166` | 名字「Frida」 |
| 141 | 26 | 任务：Recovering the Crystal | Frida · H 好宠物 `167` | 名字「Frida」 |
| 142 | 26 | 任务：Recovering the Crystal | Frida · H01A `165` | 名字「Frida」 |
| 143 | 26 | 任务：Recovering the Crystal | 龙 · 灵药 H2 `238` | 名字「Potion」 |
| 144 | 26 | 任务：Recovering the Crystal | Alice · 试衣间 灵药 `270` | 名字「Alice」 |
| 145 | 26 | 任务：Recovering the Crystal | Alice · 酒馆 H `267` | 名字「Alice」 |
| 146 | 26 | 任务：Recovering the Crystal | 女儿 · 去游泳 `293` | 名字「女儿」 |
| 147 | 26 | 任务：Recovering the Crystal | 女儿 · 去游泳（灵药） `345` | 名字「女儿」 |
| 148 | 26 | 任务：Recovering the Crystal | 女儿 · 床上1 `295` | 名字「女儿」 |
| 149 | 26 | 任务：Recovering the Crystal | 与女儿组队 `308` | 图片「Black」 |
| 150 | 26 | 任务：Recovering the Crystal | Liandra × 地精 `336` | 名字「Liandra」 |
| 151 | 26 | 任务：Recovering the Crystal | Liandra × 地精（灵药） `346` | 名字「Potion」 |
| 152 | 26 | 任务：Recovering the Crystal | Map017 · 事件6 `m17:6` | 地点「Black」 |
| 153 | 26 | 任务：Recovering the Crystal | Map025 · 事件2 `m25:2` | 地点「Black」 |
| 154 | 26 | 任务：Recovering the Crystal | Map031 · 事件9 `m31:9` | 地点「Black」 |
| 155 | 26 | 任务：Recovering the Crystal | Map047 · 事件3 `m47:3` | 地点「Black」 |
| 156 | 26 | 任务：Recovering the Crystal | Map071 · 事件34 `m71:34` | 地点「Black」 |
| 157 | 29 | 任务：The Crown of Sorcery | Erevi · 与主角 双人 `1249` | 名字「Erevi」、前置「Erevi」 |
| 158 | 29 | 任务：The Crown of Sorcery | Erevi · 床上2 `302` | 名字「Erevi」、前置「Erevi」 |
| 159 | 29 | 任务：The Crown of Sorcery | Erevi · 床上 H `1252` | 名字「Erevi」、前置「Erevi」 |
| 160 | 29 | 任务：The Crown of Sorcery | Erevi · 床上速战2 `301` | 名字「Erevi」 |
| 161 | 29 | 任务：The Crown of Sorcery | Erevi · 支配01 `18` | 名字「Erevi」 |
| 162 | 29 | 任务：The Crown of Sorcery | Erevi · 支配 H `168` | 名字「Erevi」 |
| 163 | 29 | 任务：The Crown of Sorcery | Erevi · 新婚夜 `1832` | 名字「Erevi」、前置「Erevi」 |
| 164 | 29 | 任务：The Crown of Sorcery | Erevi · 新婚夜 ED `1833` | 名字「Erevi」、前置「Erevi」 |
| 165 | 29 | 任务：The Crown of Sorcery | Erevi · 池塘 灵药 `1835` | 名字「Potion」、前置「Erevi」 |
| 166 | 29 | 任务：The Crown of Sorcery | Erevi · 绑在床上 H `1253` | 名字「Erevi」、前置「Erevi」 |
| 167 | 29 | 任务：The Crown of Sorcery | Erevi · 黑色礼服 `46` | 名字「Black」、前置「Erevi」 |
| 168 | 29 | 任务：The Crown of Sorcery | 地牢装置 · Erevi `1494` | 名字「Erevi」、前置「Alice」 |
| 169 | 29 | 任务：The Crown of Sorcery | Map030 · 事件22 `m30:22` | 地点「Erevi」 |
| 170 | 30 | 任务：学徒 | 蝙蝠饲养者 · 沙发 H `530` | 名字「Breeder」、前置「Breeder」 |
| 171 | 30 | 任务：学徒 | 地牢01 · 解放BB `532` | 前置「Breeder」 |
| 172 | 30 | 任务：学徒 | 地牢04 · 解放BB `533` | 前置「Breeder」 |
| 173 | 30 | 任务：学徒 | 地牢 · 慰藉 `821` | 前置「Breeder」 |
| 174 | 32 | 任务：蝙蝠饲养者 | 离开地精洞 `338` | 名字「Cave」、前置「Liandra」 |
| 175 | 32 | 任务：蝙蝠饲养者 | Map140 · 事件62 `m140:62` | 地点「Dungeon」、调用场景的章节 29 |
| 176 | 37 | 任务：孕妇装 | Mia · 林中相遇 `228` | 名字「Forest」、前置「Outfit」 |
| 177 | 37 | 任务：孕妇装 | Daiyu · 服装 BT `1637` | 名字「Outfit」、前置「Potion」 |
| 178 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Urakhand × Caleah `115` | 名字「Caleah」 |
| 179 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Urakhand × Caleah（回想） `127` | 名字「Caleah」 |
| 180 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · H02 `163` | 名字「Caleah」、前置「Caleah」 |
| 181 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · TF 变身 `2004` | 名字「Caleah」 |
| 182 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · 书库 H `917` | 名字「Caleah」、前置「Caleah」 |
| 183 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · 床上 `1489` | 名字「Caleah」、前置「Caleah」 |
| 184 | 42 | 任务：Orc Stronghold（又名：Orcs, Orcs, and More Orcs）任务 | Caleah · 群体 上 `808` | 名字「Caleah」、前置「Alice」 |
| 185 | 46 | 任务：与 Beth 的约会 | Erevi · 床上 `121` | 名字「Erevi」、前置「Summon」 |
| 186 | 47 | 任务：与 Mia 的约会 | 女儿 · 巨魔 `1250` | 名字「女儿」、前置「Play」 |
| 187 | 47 | 任务：与 Mia 的约会 | 女儿 · 王子 `1254` | 名字「女儿」、前置「Play」 |
| 188 | 47 | 任务：与 Mia 的约会 | 女儿们玩耍 · 序 `1285` | 名字「Play」、前置「Erevi」 |
| 189 | 53 | 任务：要有光 | Map166 · 事件39 `m166:39` | 地点「Hall」 |
| 190 | 53 | 任务：要有光 | Map167 · 事件156 `m167:156` | 地点「Hall」 |
| 191 | 53 | 任务：要有光 | 光之教会 · 事件33 `m183:33` | 地点「Diary」 |
| 192 | 54 | 任务：增强生育力 | 龙 · 战后 `203` | 名字「Dragon」 |
| 193 | 54 | 任务：增强生育力 | 龙 · 灵药 H1 `237` | 名字「Potion」、前置「Dragon」 |
| 194 | 54 | 任务：增强生育力 | 龙 · 遭遇 `202` | 名字「Dragon」 |
| 195 | 62 | 任务：Waystone 任务 第1部分 | 归还传送石 `279` | 名字「Waystone」 |
| 196 | 62 | 任务：Waystone 任务 第1部分 | Map030 · 事件7 `m30:7` | 地点「Nergal」、调用场景的章节 62 |
| 197 | 64 | 任务：给面包师的面粉 | Rosy · 强制口交 `323` | 名字「Rosy」 |
| 198 | 64 | 任务：给面包师的面粉 | Rosy · 面包店02 `333` | 名字「Rosy」、前置「Rosy」 |
| 199 | 64 | 任务：给面包师的面粉 | Rosy · 面包店03 `690` | 名字「Rosy」、前置「Rosy」 |
| 200 | 64 | 任务：给面包师的面粉 | Map065 · 事件5 `m65:5` | 地点「Black」、调用场景的章节 64 |
| 201 | 69 | 任务：叫接生婆 | Hilde · 帐篷2 `365` | 名字「Hilde」、前置「Hilde」 |
| 202 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 `366` | 名字「Hilde」 |
| 203 | 69 | 任务：叫接生婆 | Hilde · 帐篷 `360` | 名字「Hilde」、前置「Hilde」 |
| 204 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 主线 `1414` | 名字「Hilde」、前置「Hilde」 |
| 205 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 后门 `1415` | 名字「Hilde」、前置「Hilde」 |
| 206 | 69 | 任务：叫接生婆 | Hilde · 帐篷3 正常位 `1416` | 名字「Hilde」、前置「Hilde」 |
| 207 | 69 | 任务：叫接生婆 | Hilde · 帐篷3B `370` | 名字「Hilde」 |
| 208 | 69 | 任务：叫接生婆 | Hilde · 新婚夜 `357` | 名字「Hilde」 |
| 209 | 69 | 任务：叫接生婆 | Hilde · 沐浴 `359` | 名字「Hilde」、前置「Hilde」 |
| 210 | 69 | 任务：叫接生婆 | Hilde · 温泉 `1418` | 名字「Hilde」、前置「Hilde」 |
| 211 | 69 | 任务：叫接生婆 | Freyja宴 · Hilde 未中 `1486` | 名字「Hilde」、前置「Hilde」 |
| 212 | 69 | 任务：叫接生婆 | Freyja宴 · Hilde 骑乘 `1483` | 名字「Riding」、前置「Hilde」 |
| 213 | 69 | 任务：叫接生婆 | Map075 · 事件34 `m75:34` | 地点「Forest」、调用场景的章节 69 |
| 214 | 69 | 任务：叫接生婆 | Map156 · 事件34 `m156:34` | 地点「Forest」、调用场景的章节 69 |
| 215 | 71 | 任务：婚礼 | Map156 · 事件22 `m156:22` | 地点「巨人的」 |
| 216 | 75 | 任务：与 Maghda 的亲密时光 | Jenny · 奶酪 `1270` | 名字「Jenny」、前置「Jenny」 |
| 217 | 75 | 任务：与 Maghda 的亲密时光 | Jenny · 奶酪 XL `1269` | 名字「Jenny」、前置「Jenny」 |
| 218 | 75 | 任务：与 Maghda 的亲密时光 | Jenny · 手交 `732` | 名字「Jenny」、前置「Jenny」 |
| 219 | 83 | 任务：叛乱的部落 | Sequoia · H1 `476` | 名字「Sequoia」、前置「Sequoia」 |
| 220 | 83 | 任务：叛乱的部落 | Sequoia · H2 `477` | 名字「Sequoia」、前置「Sequoia」 |
| 221 | 88 | 任务：男人窝 | 地牢装置 · BB `1497` | 名字「地牢」、前置「Breeder」 |
| 222 | 88 | 任务：男人窝 | 地牢装置 · ED `1498` | 名字「地牢」、前置「Erevi」 |
| 223 | 92 | 任务：织网大师 | 蜘蛛娘 · 化人 `519` | 名字「Spider」、前置「Venomina」 |
| 224 | 92 | 任务：织网大师 | 蜘蛛洞 · 剧情3 `521` | 名字「Spider」、前置「Venomina」 |
| 225 | 92 | 任务：织网大师 | 蜘蛛洞 · 剧情4 `536` | 名字「Spider」、前置「Venomina」 |
| 226 | 92 | 任务：织网大师 | 蜘蛛洞 · 剧情5 `535` | 名字「Spider」、前置「Venomina」 |
| 227 | 92 | 任务：织网大师 | 吸血鬼受害者 Reanna 3 `669` | 名字「受害者」、前置「Black」 |
| 228 | 93 | 任务：猎巫人 | 墓园 · 夜晚 `130` | 名字「Cemetery」 |
| 229 | 93 | 任务：猎巫人 | Oksana · TF 变身 `2002` | 名字「Oksana」、前置「Oksana」 |
| 230 | 93 | 任务：猎巫人 | Oksana · 后门祭坛 H `1056` | 名字「Oksana」、前置「Heal」 |
| 231 | 93 | 任务：猎巫人 | Oksana · 地穴 H `687` | 名字「Oksana」、前置「Potion」 |
| 232 | 93 | 任务：猎巫人 | Oksana · 神殿后门 H `1052` | 名字「Temple」、前置「Oksana」 |
| 233 | 93 | 任务：猎巫人 | Oksana · 群体 上 `1070` | 名字「Oksana」、前置「Alice」 |
| 234 | 93 | 任务：猎巫人 | Map046 · 事件36 `m46:36` | 地点「Cemetery」 |
| 235 | 93 | 任务：猎巫人 | Map046 · 事件41 `m46:41` | 地点「Cemetery」 |
| 236 | 93 | 任务：猎巫人 | Map053 · 事件37 `m53:37` | 地点「Temple」、调用场景的章节 93 |
| 237 | 94 | 任务：淑女的连衣裙 | Zsofia · 卧室来访 `677` | 名字「Zsofia」、前置「Zsofia」 |
| 238 | 94 | 任务：淑女的连衣裙 | Zsofia · 墓园 H `546` | 名字「Cemetery」、前置「Zsofia」 |
| 239 | 95 | 任务：寻找旅店老板 | Oksana · 沐浴贿赂Oliver `651` | 名字「Oksana」、前置「Oliver」 |
| 240 | 96 | 任务：进一步调查 | 职责召唤 `1804` | 图片「Castle」 |
| 241 | 97 | 任务：净化者 | Adaobi · 卧室来访 `678` | 名字「Adaobi」、前置「Adaobi」 |
| 242 | 97 | 任务：净化者 | Adaobi · 礼拜堂 H `671` | 名字「Adaobi」、前置「Potion」 |
| 243 | 97 | 任务：净化者 | Reanna · 军械库口交 `686` | 名字「Reanna」 |
| 244 | 97 | 任务：净化者 | Reanna · 卧室 H `674` | 名字「Reanna」、前置「Outfit」 |
| 245 | 97 | 任务：净化者 | Reanna · 小巷2 `1646` | 名字「Reanna」、前置「Potion」 |
| 246 | 97 | 任务：净化者 | Reanna · 小巷 `1645` | 名字「Reanna」 |
| 247 | 97 | 任务：净化者 | 对峙灰港杀手 `1784` | 名字「Killer」 |
| 248 | 97 | 任务：净化者 | Map106 · 事件17 `m106:17` | 调用场景的章节 97 |
| 249 | 98 | 任务：尘归尘，土归土 | Map115 · 事件7 `m115:7` | 地点「Master」 |
| 250 | 102 | 任务：繁衍空间 | Map108 · 事件12 `m108:12` | 地点「Bakery」 |
| 251 | 108 | 任务：一笔贷款？ | 酒馆 · 掷骰 `727` | 名字「Play」、前置「Dice」 |
| 252 | 111 | 任务：遇险的母子 | 女儿 · 床上2 `297` | 名字「女儿」、前置「Room」 |
| 253 | 111 | 任务：遇险的母子 | Victoria · 白丝 怀孕（灵药） `656` | 名字「Victoria」 |
| 254 | 111 | 任务：遇险的母子 | Victoria · 红色内衣 `415` | 名字「Victoria」 |
| 255 | 111 | 任务：遇险的母子 | Victoria · 红色内衣 怀孕（灵药） `654` | 名字「Victoria」 |
| 256 | 111 | 任务：遇险的母子 | 探望 Victoria（产后） `416` | 名字「Victoria」 |
| 257 | 111 | 任务：遇险的母子 | Oksana · 沐浴 `684` | 名字「Oksana」 |
| 258 | 111 | 任务：遇险的母子 | 解锁 · 小恶魔口交 `847` | 跟随调用者 m6:6 |
| 259 | 111 | 任务：遇险的母子 | 怪木林 · 事件81 `m1:81` | 地点「Weirdwood」、调用场景的章节 111 |
| 260 | 111 | 任务：遇险的母子 | 顶层 · 事件6 `m6:6` | 地点「Black」、调用场景的章节 111 |
| 261 | 111 | 任务：遇险的母子 | 一楼 · 事件1 `m83:1` | 地点「Room」、调用场景的章节 3 |
| 262 | 111 | 任务：遇险的母子 | Map097 · 事件9 `m97:9` | 地点「Room」 |
| 263 | 113 | 任务：为了大业 | Map070 · 事件20 `m70:20` | 地点「儿童楼层」、调用场景的章节 111 |
| 264 | 115 | 任务：家族生意 | Luthien · 不在场证明 `988` | 名字「Luthien」、前置「Liandra」 |
| 265 | 115 | 任务：家族生意 | Luthien · 小屋椅子上 H `983` | 名字「Luthien」、前置「Luthien」 |
| 266 | 115 | 任务：家族生意 | Luthien · 桌上 H `997` | 名字「Luthien」、前置「Luthien」 |
| 267 | 115 | 任务：家族生意 | Luthien · 液体愉悦 `982` | 名字「Delight」 |
| 268 | 115 | 任务：家族生意 | Luthien · 胸部按摩 `998` | 名字「Luthien」 |
| 269 | 116 | 任务：任务：特殊作物 | Map019 · 事件5 `m19:5` | 地点「Stables」、调用场景的章节 3 |
| 270 | 116 | 任务：任务：特殊作物 | Map019 · 事件9 `m19:9` | 地点「Stables」、调用场景的章节 3 |
| 271 | 116 | 任务：任务：特殊作物 | Map020 · 事件9 `m20:9` | 地点「Stables」 |
| 272 | 121 | 任务：被遗弃者 | Map105 · 事件23 `m105:23` | 地点「Vampire」、调用场景的章节 97 |
| 273 | 125 | 任务：家族纽带 | Julia · 床上 `1080` | 名字「Julia」、前置「Julia」 |
| 274 | 125 | 任务：家族纽带 | Julia · 狐狸 H `1262` | 名字「Julia」、前置「Julia」 |
| 275 | 125 | 任务：家族纽带 | Julia · 第一次游泳 `1063` | 名字「Julia」 |
| 276 | 125 | 任务：家族纽带 | Julia · 第三次游泳 `1065` | 名字「Julia」 |
| 277 | 125 | 任务：家族纽带 | Julia · 第二次游泳 `1064` | 名字「Julia」 |
| 278 | 125 | 任务：家族纽带 | Julia · 谷仓 H `1264` | 名字「Julia」、前置「Julia」 |
| 279 | 125 | 任务：家族纽带 | Julia · 谷仓婚礼 `1069` | 名字「Julia」、前置「Julia」 |
| 280 | 125 | 任务：家族纽带 | Annabelle×Julia · H `1263` | 名字「Julia」、前置「Julia」 |
| 281 | 125 | 任务：家族纽带 | Map095 · 事件20 `m95:20` | 地点「家庭农场」 |
| 282 | 125 | 任务：家族纽带 | Map130 · 事件7 `m130:7` | 地点「Black」、调用场景的章节 125 |
| 283 | 125 | 任务：家族纽带 | Map131 · 事件8 `m131:8` | 地点「Black」、调用场景的章节 125 |
| 284 | 134 | 任务：神秘失踪 | Obeah · 地上 H `1157` | 名字「Obeah」、前置「Obeah」 |
| 285 | 134 | 任务：神秘失踪 | Obeah · 被俘 下 `1160` | 名字「Obeah」 |
| 286 | 134 | 任务：神秘失踪 | Obeah · 长椅 H `1154` | 名字「Obeah」、前置「Obeah」 |
| 287 | 138 | 任务：香水 | 送莲花提取物 `1275` | 名字「Extract」 |
| 288 | 151 | 任务145：成长！ | Annabelle · 挤奶 `1267` | 名字「Annabelle」、前置「Annabelle」 |
| 289 | 151 | 任务145：成长！ | Annabelle · 未中出 `1266` | 名字「Annabelle」、前置「Annabelle」 |
| 290 | 151 | 任务145：成长！ | Annabelle · 谷仓 H `1265` | 名字「Annabelle」、前置「Annabelle」 |
| 291 | 151 | 任务145：成长！ | Annabelle · 谷仓口交 `1412` | 名字「Annabelle」、前置「Annabelle」 |
| 292 | 151 | 任务145：成长！ | Julia · 挤奶 `1268` | 名字「Julia」、前置「Annabelle」 |
| 293 | 151 | 任务145：成长！ | Julia · 谷仓口交 `1411` | 名字「Julia」、前置「Annabelle」 |
| 294 | 159 | 任务156：狩猎 | Hilde · 帐篷3A `369` | 名字「Hilde」、前置「Birgitte」 |
| 295 | 159 | 任务156：狩猎 | Hilde · 帐篷3C `379` | 名字「Hilde」、前置「Birgitte」 |
| 296 | 159 | 任务156：狩猎 | 狩猎小屋 · H（大场景） `1417` | 名字「Hunting」、前置「Frida」 |
| 297 | 159 | 任务156：狩猎 | Birgitte · 小屋2 内衣 `1420` | 名字「Lingerie」、前置「Birgitte」 |
| 298 | 159 | 任务156：狩猎 | Birgitte · 小屋2 裸体 `1419` | 名字「Birgitte」、前置「Birgitte」 |
| 299 | 159 | 任务156：狩猎 | Birgitte · 椅子上 `1481` | 名字「Birgitte」、前置「Potions」 |
| 300 | 159 | 任务156：狩猎 | Freyja宴 · Birgitte 未中 `1487` | 名字「Birgitte」、前置「Birgitte」 |
| 301 | 159 | 任务156：狩猎 | Freyja宴 · Birgitte 骑乘 `1484` | 名字「Riding」、前置「Birgitte」 |
| 302 | 159 | 任务156：狩猎 | Map153 · 事件16 `m153:16` | 地点「Hunting」 |
| 303 | 159 | 任务156：狩猎 | Map155 · 事件7 `m155:7` | 地点「Birgitte」、调用场景的章节 159 |
| 304 | 159 | 任务156：狩猎 | Map156 · 事件35 `m156:35` | 地点「巨人的」、调用场景的章节 159 |
| 305 | 159 | 任务156：狩猎 | Map156 · 事件41 `m156:41` | 地点「巨人的」、调用场景的章节 159 |
| 306 | 162 | 任务159：葬礼 | Map153 · 事件17 `m153:17` | 地点「狩猎场」 |
| 307 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · DT `1643` | 名字「Daiyu」、前置「Daiyu」 |
| 308 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台1 `1634` | 名字「Daiyu」、前置「Potion」 |
| 309 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台2 `1635` | 名字「Daiyu」、前置「Potion」 |
| 310 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台1 SP `1641` | 名字「Daiyu」、前置「Potion」 |
| 311 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 后台2 SP `1642` | 名字「Daiyu」、前置「Daiyu」 |
| 312 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 服装 `1636` | 名字「Outfit」、前置「Daiyu」 |
| 313 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 清晨 `1638` | 名字「Daiyu」、前置「Daiyu」 |
| 314 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 脱衣 `1782` | 名字「Daiyu」、前置「Daiyu」 |
| 315 | 168 | 任务165：再次掩盖你的踪迹！ | Daiyu · 自慰 `1639` | 名字「Daiyu」、前置「Daiyu」 |
| 316 | 168 | 任务165：再次掩盖你的踪迹！ | Map164 · 事件8 `m164:8` | 地点「Back」、调用场景的章节 168 |
| 317 | 170 | 任务167：被绑架了！ | ED · 湿身少女 `1644` | 名字「Maiden」、前置「Potions」 |
| 318 | 170 | 任务167：被绑架了！ | ED · 脱衣 `1783` | 图片「Maiden」 |
| 319 | 175 | 任务171：爱丽丝梦游仙境 | Naamah · H1 `1495` | 名字「Naamah」、前置「Naamah」 |
| 320 | 175 | 任务171：爱丽丝梦游仙境 | Naamah · H2 `1496` | 名字「Naamah」、前置「Naamah」 |
| 321 | 175 | 任务171：爱丽丝梦游仙境 | Naamah · H3 `1836` | 名字「Naamah」、前置「Naamah」 |
| 322 | 175 | 任务171：爱丽丝梦游仙境 | Map166 · 事件41 `m166:41` | 地点「Hall」、调用场景的章节 175 |
| 323 | 179 | 任务176：热门八卦 | Vix · 火山口1 `1632` | 名字「Vix」、前置「Vixenatrix」 |
| 324 | 179 | 任务176：热门八卦 | Vix · 火山口2 `1633` | 名字「Vix」、前置「Vixenatrix」 |
| 325 | 181 | 任务178：偷巢者！ | Tabufa · 卧室 `1631` | 名字「Tabufa」、前置「Tabufa」 |
| 326 | 181 | 任务178：偷巢者！ | Tabufa · 口交 `1500` | 名字「Tabufa」、前置「Tabufa」 |
| 327 | 181 | 任务178：偷巢者！ | Tabufa · 王座 `1499` | 名字「Tabufa」、前置「Tabufa」 |
| 328 | 185 | 任务182：护送 | Map175 · 事件89 `m175:89` | 地点「内城」 |
| 329 | 188 | 任务185：承诺 | Erevi · 床上速战 `44` | 名字「Erevi」 |
| 330 | 188 | 任务185：承诺 | Erevi · 红色内衣（灵药） `652` | 名字「Potion」 |
| 331 | 188 | 任务185：承诺 | Victoria · 剧情02 灵药 `147` | 名字「Potion」 |
| 332 | 188 | 任务185：承诺 | Victoria · 黑色内衣 怀孕（灵药） `655` | 名字「Victoria」 |
| 333 | 188 | 任务185：承诺 | Josephine · 卧室 `1650` | 名字「Bedroom」、前置「Potion」 |
| 334 | 188 | 任务185：承诺 | Yvette · 新婚夜（大场景） `1657` | 名字「Wedding」、前置「Potion」 |
| 335 | 188 | 任务185：承诺 | Cathrine · 卧室4 `1659` | 名字「Bedroom」、前置「Potions」 |
| 336 | 188 | 任务185：承诺 | 同床 `1803` | 图片「Wedding」 |
| 337 | 188 | 任务185：承诺 | Map128 · 事件22 `m128:22` | 地点「Barn」、调用场景的章节 125 |
| 338 | 190 | 任务187：开膛手 | Mia · 床上 H1 `232` | 名字「Mia」 |
| 339 | 190 | 任务187：开膛手 | Mia · 床上 H1（灵药） `919` | 名字「Potion」 |
| 340 | 190 | 任务187：开膛手 | Jenny · 初次怀孕 `742` | 名字「Jenny」 |
| 341 | 190 | 任务187：开膛手 | Jenny · 手交（无Tom） `750` | 名字「Jenny」 |
| 342 | 190 | 任务187：开膛手 | Tom · 第一次输 下 `754` | 名字「Tom」 |
| 343 | 190 | 任务187：开膛手 | Tom · 第三次输 下 `756` | 名字「Tom」 |
| 344 | 190 | 任务187：开膛手 | Tom · 第二次输 下 `755` | 名字「Tom」 |
| 345 | 191 | 任务188：锦标赛 | Yvette · PG5 `1821` | 名字「Yvette」、前置「Potion」 |
| 346 | 191 | 任务188：锦标赛 | Yvette · 假做 H `1654` | 名字「Yvette」、前置「Yvette」 |
| 347 | 191 | 任务188：锦标赛 | Yvette · 泳池 `1824` | 名字「Yvette」、前置「Yvette」 |
| 348 | 191 | 任务188：锦标赛 | Yvette · 泳池花园 H `1805` | 名字「Yvette」、前置「Yvette」 |
| 349 | 191 | 任务188：锦标赛 | Yvette · 自慰1 `1647` | 名字「Yvette」、前置「Yvette」 |
| 350 | 191 | 任务188：锦标赛 | Yvette · 自慰2 `1648` | 名字「Yvette」、前置「Yvette」 |
| 351 | 191 | 任务188：锦标赛 | Yvette · 调教 上 `1652` | 名字「Yvette」、前置「Yvette」 |
| 352 | 191 | 任务188：锦标赛 | Yvette · 调教 口交 `1653` | 名字「Yvette」、前置「Yvette」 |
| 353 | 191 | 任务188：锦标赛 | 灰港城堡 · 事件8 `m180:8` | 地点「Greyport」、调用场景的章节 191 |
| 354 | 196 | 任务193：中暑 | Josephine · 卧室 MM `1651` | 名字「Josephine」 |
| 355 | 196 | 任务193：中暑 | Josephine · 厨房 `1656` | 名字「Josephine」、前置「Wedding」 |
| 356 | 196 | 任务193：中暑 | Josephine · 泳池 `1649` | 名字「Josephine」、前置「Josephine」 |
| 357 | 196 | 任务193：中暑 | Josephine · 王座 `1660` | 名字「Josephine」、前置「Josephine」 |
| 358 | 196 | 任务193：中暑 | 初次游泳（大场景） `1795` | 跟随调用者 m180:15、m180:50 |
| 359 | 196 | 任务193：中暑 | 灰港城堡 · 事件15 `m180:15` | 地点「Greyport」、调用场景的章节 196 |
| 360 | 196 | 任务193：中暑 | 灰港城堡 · 事件50 `m180:50` | 地点「Greyport」、调用场景的章节 196 |
| 361 | 197 | 任务194：Cathrine 修女 | Cathrine · 卧室3 `1658` | 名字「Bedroom」、前置「Cathrine」 |
| 362 | 197 | 任务194：Cathrine 修女 | Cathrine · 卧室5 `1822` | 名字「Bedroom」、前置「Cathrine」 |
| 363 | 197 | 任务194：Cathrine 修女 | Cathrine · 床上 `1825` | 名字「Cathrine」、前置「Cathrine」 |
| 364 | 197 | 任务194：Cathrine 修女 | Cathrine · 手交 `1655` | 名字「Cathrine」、前置「Cathrine」 |
| 365 | 197 | 任务194：Cathrine 修女 | Cathrine · 祭坛 PG `1827` | 名字「Cathrine」、前置「Phallus」 |
| 366 | 197 | 任务194：Cathrine 修女 | Cathrine · 祭坛 序 `1826` | 名字「Cathrine」、前置「Cathrine」 |
| 367 | 197 | 任务194：Cathrine 修女 | Cathrine · 祭坛 无PG `1828` | 名字「Cathrine」、前置「Cathrine」 |
| 368 | 198 | 任务195：神秘陌生人 | Baron · 登场 `1794` | 名字「Baron」 |
| 369 | 198 | 任务195：神秘陌生人 | Baron · 训斥 `1801` | 名字「Baron」 |
| 370 | 198 | 任务195：神秘陌生人 | Map181 · 事件15 `m181:15` | 地点「Tower」、调用场景的章节 198 |
| 371 | 205 | 任务201：意志之战 | 水蛭袭击 `157` | 名字「Attack」 |
| 372 | 205 | 任务201：意志之战 | 骑士袭击 `496` | 名字「Attack」、前置「Shakala」 |
| 373 | 211 | 任务207：讨厌的野兽 | Map188 · 事件16 `m188:16` | 地点「Unicorn」 |
| 374 | 212 | 任务208：Enchanted Forest | 精灵 · 之后 `1831` | 名字「精灵」 |
| 375 | 212 | 任务208：Enchanted Forest | 精灵 · 初次 `1830` | 名字「精灵」 |
| 376 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满1 H `1241` | 名字「蝙蝠洞」、前置「Breeder」 |
| 377 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满2 H `1245` | 名字「蝙蝠洞」、前置「Breeder」 |
| 378 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满1 NP H `1242` | 名字「蝙蝠洞」、前置「Breeder」 |
| 379 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 丰满2 NP H `1246` | 名字「蝙蝠洞」、前置「Breeder」 |
| 380 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小1 H `1243` | 名字「蝙蝠洞」、前置「Breeder」 |
| 381 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小2 H `1247` | 名字「蝙蝠洞」、前置「Breeder」 |
| 382 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小1 NP H `1244` | 名字「蝙蝠洞」、前置「Breeder」 |
| 383 | 216 | 任务212：是个男孩 | 蝙蝠洞 · 娇小2 NP H `1248` | 名字「蝙蝠洞」、前置「Breeder」 |
| 384 | — | （未定位） | Map170 · 事件7 `m170:7` | — |
| 385 | — | （未定位） | Map171 · 事件13 `m171:13` | — |
| 386 | — | （未定位） | Map182 · 事件25 `m182:25` | — |
