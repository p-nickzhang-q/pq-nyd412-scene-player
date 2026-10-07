# 更新日志

## v2.4.0

### 改进：剧情顺序改为依据游戏自己的 215 个任务表
- **上一版的问题**（用户实测反馈）：「感觉你像是把同一人物的放在一起了，而不是按剧情顺序」。
  原因：v2.2.0 只用「人物名在攻略里**首次出现**的章节」定位，于是同一个人物的所有场景
  都挤在同一章 —— 那本质是**按人物分组**，不是按剧情推进。
- **新依据**：`YEP_QuestJournal` + `YEP_X_MoreQuests1` 里定义了 **215 个任务**，
  任务编号顺序就是剧情顺序（和攻略的 `任务212：是个男孩` 编号一致）。这比攻略正文可靠得多，
  因为每个任务都带**标题 / 委托人 / 地点 / 描述**。
- **新增 `tools/quest_names.py`**：中英对照表。场景名是英文（`Julia · 挤奶`），
  任务元数据是中文（`Quest 153 挤奶女 / From 朱莉娅 / Location 家族农场`），
  没有这张表就只能退回「人物名」这个粗信号。含人名 92 条、地点 21 条、概念词 80 条。
- **打分制匹配**（`tools/story_order.py`）：子标签命中任务标题（权重最高，
  `Julia · 挤奶` → 任务153）、人物名/地点名对照、前置条件里的概念词
  （开关 `HildeBathing` → 「洗澡」、`MilkingStage` → 「挤奶」，按稀有度加权）、图片文件名。
  概念词只在**和人物一起**出现在同一任务里时才加分（单看概念会到处误配）。
- **同任务内按作者写场景的顺序排**：用场景测的**人物专属变量 id**（基本跟着剧情走）。
  实测 Victoria：剧情01→02→03→(196)裸体→(199)怀孕→(419)内衣怀孕；
  Hilde：(96)温泉→(361)帐篷→沐浴→帐篷2→(1307)帐篷3；
  Julia：(648)谷仓H→(683)床上→(988)谷仓婚礼→(1259)狐狸H。
- 结果：288/306 已定位（分布在 63 个任务里）。**局限**：任务元数据里没有区分
  同一人物多个 H 场景属于哪个任务的信息，所以同人物的场景仍会落在同一任务里，
  靠变量 id 排先后；要挪动用 `params/storyOverrides.json`。
- 列表第二行的标签由「剧情N」改为「任务N」（就是游戏任务表里的编号）。


## v2.3.0

### 变更：清单不再收录 80 个「地图事件场景」
- 需求：地图事件在连播时表现为「画面在地图之间跳」，不要这些条目。
- 做法：`python3 tools/setup.py <游戏目录> --yes --no-maps`（`--no-maps` 是既有开关，
  **可逆**：去掉它重跑就恢复）。清单 386 → **306** 项，其中子场景 27 个默认隐藏，
  列表默认显示 **279** 项。
- **但要说清楚**：这 80 个并不是传送触发器 —— 每个都有 24~64 张图片、几十到三百多行对白，
  包括 `Map060#61` 决战内尔伽勒、`Map020#9` Beth 马厩 H、`m8:3` 魔法之井（64 图 315 行对白）。
  不收录的真实理由是「播放会真的把玩家传送走」。播放代码（`reserveTransfer` → 落地 →
  `event.start()`）与相关测试都保留，恢复后即可用。
- 连带影响：`F6` 的「杂项」分类现在是空的（那 6 个杂项全是地图事件）；缺素材场景 39 → 30 个。
- 修 `setup.py` 的一个顺序 bug：剧情顺序是在写入新参数**之前**算的，却从 `plugins.js`
  读清单，于是算进了上一次的旧数据（删掉地图事件后 `storyOrder` 里还留着 80 个地图键）。
  现在把刚扫出来的清单直接传给 `story_order.compute()`。
- 冒烟测试：地图相关用例在地图场景为空时自动跳过（100 项断言；收录时为 122 项）。


## v2.2.0

### 新增：列表默认按剧情顺序排列
- **问题**：列表按公共事件 id 排（作者的创建顺序），**不等于剧情顺序** ——
  有些后期剧情的场景 id 很小，排在很前面。
- **依据**：游戏自带中文攻略 —— `PQ_NYD_v3.71_full_walkthrough.zh.md` 第 12 节约 188 个任务
  **本身就是按剧情推进写的**，后续补丁攻略（NYD375/381/391/395/401/410）是 186~215 号任务，
  按版本接在后面，拼成 1~219 的章节表。
- **新增 `tools/story_order.py`**：给每个场景定位章节，用了 5 个信号 ——
  人物/地点名在攻略里首次出现的位置、场景前置条件（指令 111 引用的开关/变量名，如
  `CathrineNoCurse`）、图片文件名（`FreyjaHall - 001`）、**同义词表**（我们「北方森林」/
  攻略「北部森林」、我们「魔法之井」/ 攻略「圣井」、我们「灰港城堡」/ 攻略「Greyport」、
  「地精女儿」/「Female Goblin」）、以及子场景跟随调用者。
  最终章节 = `max(人物线起点, 最晚前置条件章节)`。
  **383 / 386 已定位**；剩下 3 个城堡内部小事件（废弃厨房/熊穴出口/第一层）攻略里没有对应说法，
  排在最后而不是瞎猜。
- **插件**：新增参数 `storyOrder`（`[[场景键,章节号],...]`）、`storyChapters`（章节标题）、
  `sortKey`（默认 114 = **F3**）。默认按剧情排；`F3` 切回 id 顺序。
  每项第二行显示所属章节（`剧情3 与所有村民交谈`）。
- **可订正**：`params/storyOverrides.json`（`{"场景键": 章节号}`）优先级最高，改完重跑 setup.py。
  逐条的定位依据见新增的 `STORY_ORDER.md`。
- 修两个隐蔽问题：① `chapter_of` 里中文 n-gram 扩展用了 `sorted(set)`，
  长度相同的候选顺序受 `PYTHONHASHSEED` 影响 → **跨进程结果不稳定**（同一份数据两次生成顺序不同）；
  ② 2 字片段会误配（`第一层酒馆` 切出 `第一` → 误判到第 1 章）。现在候选按「长度降序、字典序」排，
  且只切 3~4 字片段。
- 冒烟测试 105 → **122** 项（新增剧情排序一节：默认排序、F3 切换、章节显示、与筛选/子场景叠加、连播跟随）。


## v2.1.0

### 新增：子场景（嵌套）默认不显示
- **问题**：本作有大量场景在内部又调用了别的场景。例如 `#1414 Hilde · 帐篷3 主线` 会调用
  `#1415/#1416`；`#264 Alice × Johan 桌边` 含 `#297 女儿 · 床上2`。这些被调用的场景同时
  也单独占列表一项，连播时就会「大场景播一遍、里面的小场景又单独播一遍」，看起来像重复。
- **新增 `tools/nesting.py`**：沿指令 117（调用公共事件）把嵌套关系全查出来 ——
  306 个公共事件场景里 **81 个**是被别的场景调用的（H 77 / 剧情 4），地图场景不参与。
  列表默认显示 **305** 项（原 386）。
- **环保护**：`#1260 Caleah · 酿酒 H` ↔ `#1261 Alice · 酿酒 H` 互相调用且没有环外入口，
  全隐藏会彻底没有入口，因此保留 id 最小的 `#1260` 可见。检测时会打印这条。
- **插件**：新增参数 `subScenes`（自动生成）与 `subKey`（默认 115 = **F4**）。
  默认隐藏子场景；按 `F4` 临时显示，显示时该行标 `⊂子场景`，第二行写明「⊂ 被『XX』调用」。
  子场景与 `F6` 类型筛选是两个独立维度，可叠加（如「仅H + 隐藏子场景」）。
- **`SCENES.md` 改为可再生成**：新增 `tools/make_scenes_md.py`（此前那份是手写的，无法重建），
  并加了「子场景」列。生成器已逐列比对确认能复现原文件的全部字段。
- 冒烟测试断言数 87 → **105**（新增子场景一节：默认隐藏/切换/与筛选叠加/环保护/绘制标记）。


## v2.0.2

### 修复：F10 自动推进对话会一直重复当前对话
- **根因**：MV 的 `Window_Message.onEndOfText()` 在文本播完后会把 `_textState` 置为 `null` 并
  `startPause()`（`_waitCount = 10; pause = true`）。玩家按确定键时 `updateInput()` 做的是：
  ```js
  this.pause = false;
  if (!this._textState) { this.terminateMessage(); }   // close() + $gameMessage.clear()
  ```
  v2.0.0/v2.0.1 **只清了 `pause`，没跟着 `terminateMessage()`**，于是 `$gameMessage` 仍是 busy，
  下一帧 `canStart()` 又 `startMessage()` —— 表现就是同一段对话反复播。
- **修复**：新增 `SP.advanceMessage(mw)`，一字不差复刻上面那个分支（`_textState` 非 null 时只清
  `pause`，例如 `\|` 等待码的中途暂停，不 terminate）。
- **测试**：冒烟测试补上「自动推进对话」一节（v2.0.1 重写测试时漏掉了这一节，所以这个 bug 没被
  抓住），并用一个按 `rpg_windows.js` 分支顺序建模的迷你 `Window_Message` 复现「重复对话」；
  另有一条对照断言：只清 `pause` 时确实会重复，证明该测试有效。断言数 76 → 87。


## v2.0.1

### 修复：播放地图场景时崩溃
```
Uncaught TypeError: Cannot read property 'list' of undefined
    at Game_Event.list (rpg_objects.js:8470)
    at Object.SP.startMapEvent (ScenePlayer.js:503)
```
- **根因**：MV 的 `Game_Event.prototype.list()` 是 `this.page().list`，而 `page()` 是
  `this.event().pages[this._pageIndex]`；当**没有任何事件页的条件满足**时
  `findProperPageIndex()` 返回 `-1`，`page()` 就是 `undefined`，直接调 `list()` 必抛。
  地图事件大量用开关/变量卡页条件，所以很容易踩到。
- **修复**：新增 `SP.pageListOf(ev)` 统一安全取指令表 —— 先试 `page()`（并兜住异常与 `page.list` 缺失），
  没有 `page()` 的非标准实现回退到 `list()`（同样兜异常）；`startMapEvent` 改用它，
  页条件未满足时提示「当前没有生效的事件页（页条件未满足），跳过」而不是崩。
- 顺手给按键处理器加了 try/catch：单个场景出错不再把异常抛到全局。
- **测试**：测试桩补上 `page()`（此前 fake event 没有 `page()`，掩盖了这条路径）；
  新增 6 项回归断言，其中 `mkEvent(null,false)` 用与 MV 一字不差的 `list()` 实现复现该崩溃。
  断言数 69 → 76。
- **测试脚本入库**：`tools/smoke_test.js`（此前只在 /tmp，被系统清理过一次）。


## v2.0.0

> 已在游戏内实测：缺影片场景不再卡顿。

### 修复：播放时卡住（缺影片）
- **根因**：MV 的 `Graphics._playVideo` 把 `onerror` 接到重试加载器
  （`ResourceHandler._defaultRetryInterval = [500, 1000, 3000]`），且 `_videoLoading = true` 让
  `isVideoPlaying()` 恒为真、解释器卡在 `waitMode 'video'`。**每个缺失影片卡约 4.5 秒**。
  本作 923 个影片引用里有 100 个文件不存在，`Beth · 求欢1` 一个场景就缺 12 个（≈54 秒）。
- **修复**：缺素材检测从「只查图片（指令 231）」扩展到「也查影片（指令 261）」，
  影片项在 `missingAssets` 里带 `movie:` 前缀；插件运行时同时索引 `img/pictures` 与 `movies`。
  受影响场景从 30 个升到 39 个（其中 23 个含缺失影片）。

### 新增：地图事件场景（80 个）
- 地图事件的指令在 `pages[].list`，无法用 `reserveCommonEvent`。播放流程：先
  `reserveTransfer` 传送到目标地图 → 等落地（最长 10 秒，超时放弃）→ `event.start()`
  只设 `_starting`，由 MV 的 `Game_Map.setupStartingMapEvent()` 完成解释器 setup 与结束后的 unlock。
- 防重复触发：事件已 `isStarting()` / 落地时触发了「玩家接触」型事件 / 已有事件在跑 → 不再 `start()`。
- 新增 `mapScenes` 参数与 `ScenePlayer.playMap(mapId, eventId)`。

### 新增：类型标签与筛选
- `tags` 参数（386 条）：`h` / `story` / `misc`；`F6`（keyCode 117）循环切换筛选，
  列表显示 `[H]`/`[剧情]`/`[杂项]`，**自动连播只在当前筛选内**。
- 标签由 `tools/tagging.py` 的**显式表**给出：本作绝大多数场景本身含性内容，所以 H 是默认，
  剧情/杂项逐条看过台词后确认（自动分类器试过，会把 80%+ 判成 H，不可用）。
- 内部模型重构为 `SP.items`（全部）+ `SP.view`（当前筛选），所有位置参数相对 `SP.view`；
  切换筛选时按 `lastKey` 重新定位光标与「上次播放」。

### 工具
- `scan_game.py`：新增 `--maps` / `--map-min-pics` / `--map-triggers`；抽出 `collect()` 供两个工具共用；
  新增 `closure_assets()`（图片+影片）与 `movie_index()`；输出 `mapScenes` 与 `tags`。
- `setup.py`：改用 `collect()`，写入 `mapScenes` / `tags` / `filterKey`，新增 `--no-maps`。


## v1.2.0（场景清单扩充）

- **场景清单 162 → 306**：新增口径「像顶层场景的」（有图 + 有对白 + 不被其它事件用指令 117 调用 +
  `trigger=0`，且图片数 ≥4 或名字带场景感关键词，排除剧情枢纽与 `Anim*` 子事件），补进 140 个
  名字不含 `Scene` 的独立场景（`MiaSexInBed1`、`CaleahZivaSex`、`ZsofiaSexInCemetery`、
  `AskBethForSex1`、`MassZivaPart1`、`DST01BBSetFree` 等）。
- `GDScene01-03` 从排除名单收回（是 13 张图的真场景）；排除名单从 8 个收窄到 5 个真正非 CG 的
  （`410` SceneIntro、`411` SceneExtro、`1894-1896` AnimPixieScene1-Cam1/2/3）。
- **缺素材场景 15 → 30**（526 → 884 个缺失文件名），`unlockEvents` 147 → 276。
- `tools/scan_game.py` 新增 `--mode scene|auto|all-pics` 与 `--min-pics`。
- `tools/setup.py` 重构为**复用 `scan_game` 的扫描逻辑**（新增 `--mode` / `--min-pics`），
  两个工具的口径不会再漂移。
- 实测仍不覆盖：含「显示图片」的**地图事件** 309 个（指令在 `pages[].list`，本插件按公共事件 id 触发）。


## v1.1.0（仓库整理）

- 仓库定位改为**《农民的任务》NYD412 专用**：README 全面改写为本作视角（引擎实为 MV、
  本作 `ListenToF8.js` 改过按键、目录结构为 `www/`、可选内容包未安装等实测结论）。
- 新增 `params/`：`sceneList.json`（162 项）、`missingAssets.json`（15 场景 526 个缺失文件名）、
  `names.zh.json`（中文名映射）、`plugins-entry.txt`（可直接粘进 `www/js/plugins.js` 的整行）。
- 新增 `SCENES.md`：162 个场景对照表（id / 中文名 / 原名 / 指令数 / 首句 / 缺素材）。
- 仓库名改为 `pq-nyd412-scene-player`。
- 新增 `tools/fix-unlock-events.py`：修正作弊菜单（`VirtualacgPC`）的 `unlockEvents`，
  剔除缺素材的场景 id（162 -> 147），支持 `--dry-run` / `--restore` / `--drop`；
  自动备份（同一秒多次运行也不会互相覆盖）、写入后回读校验、可重复执行。
  已在副本上验证 147 -> 162 -> 147 往返后与目标文件逐字节一致。

## v1.1.0

- **新增：缺素材检测**。`missingAssets` 参数（`{"场景id":["图片名",...]}`）配合运行时目录索引：
  - NW.js 下用 `require('fs')` 读 `img/pictures` 建立文件名索引，先探测 `BlackImage` 自检目录是否正确（`www/img/pictures/` 与 `img/pictures/` 两种布局都尝试），失败则退回离线清单；
  - 列表里缺素材项标红 + `⚠缺素材`，第二行显示缺多少张、缺的第一张叫什么；
  - 手动播放会被拒绝并提示；**自动连播自动跳过**这些场景；
  - 若全部场景都不可播，自动连播停止并提示，不再每帧重试刷屏；
  - 素材补上后**自动放行**，无需改配置。
- 新增 `ScenePlayer.checkAssets()`：打印缺素材报告。
- 新增 `tools/scan_game.py`：扫描 MV 游戏，自动生成 `sceneList` / `missingAssets`（沿指令 117 递归收集图片，能把被场景调用的子事件缺图也算出来）。
- 新增 `ScenePlayer.playPrev()`；`playNext` / `playPrev` 统一走 `findPlayable()`，会跳过缺素材项并正确回绕。

## v1.0.1

- **修复崩溃**：`TypeError: Cannot read property 'length' of undefined` at `Window_SceneList.maxItems`。
  MV 的 `Window_Selectable.prototype.initialize` 末尾会执行
  `deactivate() → reselect() → select() → ensureCursorVisible() → maxTopRow() → maxRows() → maxItems()`，
  而 v1.0.0 是「先调父类、后初始化 `this._data`」，那一刻 `_data` 仍是 `undefined`。
  现改为**先初始化 `_data = []` 再调父类**（与 MV 自带的 `Window_Command` 先 `this._list = []` 同一模式），
  并给 `maxItems()` 加了兜底。
- 测试桩改为**逐行复刻** MV 的 `Window_Selectable` 调用链；改桩后该崩溃可被测试稳定复现（回归测试已加入）。

## v1.0.0

- 首个版本：
  - `F7` 场景列表窗口（↑↓ / ←→ 跳 10 / PgUp·PgDn / Home·End / Enter / Esc）；
  - `F8` 单键播放下一个；
  - `F9` 自动连播（场景结束后自动接下一个，间隔可配）；
  - `F10` 自动推进对话（仅在文本显示完整且无选项/数字输入时翻页）；
  - 每项两行显示：自定义名 + 原始事件名，选中/上次播放/缺素材三种配色；
  - `sceneList` 支持 `[id]` / `[id, 名称]` / `[id, 名称, 原名]`；
  - 事件运行中拒绝重入，避免叠事件；
  - 控制台 API：`play` / `playNext` / `playId` / `toggleAuto` / `toggleMsgAuto` / `status` / `scenes`。
