# 《农民的任务》NYD412 — 场景速播器（ScenePlayer）

给 **《农民的任务》**（Peasant's Quest，本作构建版本 **NYD412**）用的 RPG Maker MV 插件：不用再在游戏菜单里一个个点，按一个键连着看场景，或者全自动连播。

**本仓库是这款游戏专用的**，不是通用插件：

- 已内置本作 **306 个场景**的清单（含中文名）；
- 已内置本作 **30 个缺素材场景**的清单 —— 这些场景依赖未安装的可选内容包（Spicy Mod），触发会直接把游戏打成 `Loading Error`，插件会标 ⚠ 并自动跳过；
- 安装步骤、FAQ 都是按本作的目录结构和插件环境写的。

场景全表见 **[SCENES.md](SCENES.md)**。

## 覆盖范围

清单来自 `tools/scan_game.py --mode auto`，两条口径取并集：

1. **事件名含 `Scene`**（再剔除 5 个真正非 CG 的：`410` SceneIntro、`411` SceneExtro、`1894-1896` AnimPixieScene1-Cam1/2/3）；
2. **「像顶层场景」的**：有图片 + 有对白 + 不被其它事件调用（指令 117）+ `trigger=0`，且图片数 ≥4 或名字带场景感关键词，并排除剧情枢纽（`*Dialogue`/`*Quest`/`*Announce*`/`Grow*` 等）。

| 口径 | 数量 |
|---|---|
| 公共事件总数 | 2040 |
| 含「显示图片」的公共事件 | 1207 |
| 名字含 `Scene`（口径 1） | 166 |
| 「像顶层场景」（口径 2 新增） | 140 |
| **本清单合计** | **306** |
| 含「显示图片」的**地图事件**（未覆盖） | 309（其中 93 个含 ≥5 张图） |
| `Anim*` 动画子事件（故意不收录） | 60+ |

**仍然不是「全部」**：本插件按**公共事件 id** 触发，覆盖不到指令写在 `pages[].list` 里的**地图事件**（`Map008` 事件#3 有 1779 条指令 64 张图这类）。`Anim*` 是场景内部调用的动画子事件，单独播通常没有画面，故意不收。

如需再扩口径：`--mode all-pics` 会把 1207 个含图片的事件全列进来（含大量子事件，不建议）。

## 先了解本作的几个坑

这几点都是实测踩出来的，装插件前值得一看：

| 事实 | 影响 |
|---|---|
| **引擎实际是 RPG Maker MV**（`RPGMAKER_NAME === 'MV'`），尽管本作自带的 `VirtualacgPC.js` 插件头部写着 `@target MZ` —— 那是移植作者标错了 | 所以本插件是 MV 版；别拿 MZ 插件往上套 |
| 本作自带 `ListenToF8.js`，它**整体改写**了 `SceneManager.onKeyDown`：只保留 F5 重载，**F8 不再打开开发者工具** | 所以 F8 可以安全用作「播放下一个」（标准 MV 里 F8 是 devtools，会冲突） |
| 游戏目录结构是 `<游戏根目录>/www/js/plugins/`（根目录 `package.json` 的 `main` 是 `www/index.html`） | 插件要放到 `www/js/plugins/`，参数写在 `www/js/plugins.js` |
| 本作未安装可选内容包（Spicy Mod） | 30 个场景的图片文件根本不存在，触发即 `Loading Error`；本仓库的 `params/missingAssets.json` 就是这份清单 |
| 场景的对话文本已汉化，但事件名仍是英文（`SexSceneAliceTF` 之类） | 所以本插件支持给每个场景配中文显示名，仓库里已配好 |

---

## 功能

| 功能 | 说明 |
|---|---|
| **F7 场景列表** | 键盘驱动的列表窗：翻页、跳转、直接播放选中项。每项两行显示（中文名 + 英文原名） |
| **F8 单键下一个** | 不开任何菜单，按一下播下一个场景；连按就是连着看 |
| **F9 自动连播** | 当前场景一结束，自动接下一个（间隔可配） |
| **F10 自动推进对话** | 对话显示完整后自动翻页；**遇到选项/数字输入绝不替你选** |
| **缺素材检测** | 启动后读取 `img/pictures` 建索引，本作那 30 个缺图场景标红 ⚠、拒绝播放、自动连播时跳过 |
| **控制台 API** | `ScenePlayer.playId(1257)` 之类，方便脚本化调试 |

设计上刻意保守：只做「触发公共事件」，**不直接改存档数据**；事件/对话运行中不会重入，避免叠事件。

---

## 安装

### 1. 放入插件文件

```
<游戏根目录>/www/js/plugins/ScenePlayer.js
```

### 2. 在 `www/js/plugins.js` 注册

打开 `<游戏根目录>/www/js/plugins.js`，把 **[`params/plugins-entry.txt`](params/plugins-entry.txt)** 里的那一行**整行**粘到 `var $plugins = [ ... ]` 数组的**末尾**（注意末尾逗号；若你插在最后一项之后，那一项原本没有逗号，需要自己补一个）。

粘完形如：

```js
  {"name":"MyPlugin", ... },
  {"name":"ScenePlayer","status":true,"description":"...","parameters":{
    "sceneList":"[[10,\"Ziva · 剧情01\",\"ZivaScene01\"], ... ]",
    "openKey":"118","nextKey":"119","autoKey":"120","msgKey":"121",
    "autoDelay":"60","msgDelay":"45","missingAssets":"{\"295\":[\"DaughterBedScene - 001\", ...]}"}},
```

粘完可以验一下语法（本作插件目录里已有很多条目，别破坏结构）：

```bash
node --check www/js/plugins.js
```

### 3. 重启游戏

MV 只在启动时读插件，必须重启 `Game.exe`（或按 `F5` 重载）才生效。

### 卸载

删掉 `www/js/plugins/ScenePlayer.js`，并删除 `www/js/plugins.js` 里 `"name":"ScenePlayer"` 那条（或把 `"status"` 改成 `false` 临时禁用）。

---

## 使用方法

### 快捷键（在场景地图上生效）

| 按键 | 作用 |
|---|---|
| `F7` | 打开场景列表窗口 |
| `F8` | 直接播放下一个场景（连按＝连着看） |
| `F9` | 自动连播开/关：当前场景结束后自动接下一个 |
| `F10` | 自动推进对话开/关：对话显示完自动翻页 |

`F9` + `F10` 一起开，就是**全自动当动画看**。

### 列表窗口内

| 按键 | 作用 |
|---|---|
| `↑` `↓` | 上下选择 |
| `←` `→` | 一次跳 10 个 |
| `PgUp` `PgDn` | 翻页 |
| `Home` `End` | 跳到首/尾 |
| `Enter` | 播放选中场景并关闭窗口 |
| `Esc` | 关闭窗口 |

配色：选中＝蓝，上次播放＝橙，**缺素材＝红 + `⚠缺素材`**（第二行显示缺多少张、缺的第一张叫什么）。

### 控制台 API

游戏里按 `F12` 打开开发者工具，Console 里：

```js
ScenePlayer.playNext()        // 播放下一个
ScenePlayer.playPrev()        // 播放上一个
ScenePlayer.play(67)          // 播放列表第 68 项（0 起）
ScenePlayer.playId(1257)      // 按公共事件 id 播放（不在列表里也能播）
ScenePlayer.toggleAuto()      // 切换自动连播
ScenePlayer.toggleMsgAuto()   // 切换自动推进对话
ScenePlayer.status()          // 打印当前状态
ScenePlayer.checkAssets()     // 打印缺素材报告
ScenePlayer.scenes            // 当前场景列表
```

---

## 缺素材检测

本作未安装可选内容包（Spicy Mod），**306 个场景里有 30 个**的图片文件不存在（共 884 张），触发即：

```
Loading Error
Failed to load: img/pictures/DaughterBedScene - 001.png
Missing Spicy Mod detected: ...
```

`Retry` 没用（文件本来就不存在），只能重启游戏。

插件对此的处理：

1. 首次需要时读取 `img/pictures` 建文件名索引（**不是开机时**，不拖慢启动）；
2. 先用一张必然存在的通用图（`BlackImage`）自检目录找对了没，`www/img/pictures/` 和 `img/pictures/` 两种布局都试，找不到就退回 `params/missingAssets.json` 里的离线清单；
3. 只拦**确实缺失**的：列表标 ⚠、手动播放被拒并提示、自动连播自动跳过（本作 #295/297/298 连缺三个，会一次跳到 #340）；
4. 全部不可播时自动连播停下并提示，不会每帧重试刷屏；
5. **以后装上 Spicy Mod 会自动放行**，不需要改配置（每次实时查文件）。

30 个受影响场景：

| id | 中文名 | 缺图数 | 素材族 |
|---|---|---|---|
| 291 | Victoria × 女儿 | 39 | MCBedroom4 |
| 293 | 女儿 · 去游泳 | 27 | Bathing |
| 295 | 女儿 · 床上1 | 23 | DaughterBedScene, DaughterBedScene2, DaughterBedSceneP |
| 297 | 女儿 · 床上2 | 27 | DaughterBedScene, DaughterBedScene2, DaughterBedSceneP |
| 298 | 女儿 · 床上3 | 13 | DaughterBedScene2B, DaughterBedSceneB |
| 301 | Erevi · 床上速战2 | 6 | BedroomTOD |
| 304 | Erevi × 女儿 | 19 | BedroomTOD5 |
| 309 | Victoria × 女儿（灵药） | 39 | MCBedroom4 |
| 345 | 女儿 · 去游泳（灵药） | 27 | Bathing |
| 482 | 观看地精女儿 阶段1 | 4 | GoblinDaughterWoods |
| 483 | 观看地精女儿 阶段2 | 5 | GoblinDaughterWoods |
| 487 | 地精女儿 · 剧情01 | 3 | GoblinDaughterWoods3 |
| 488 | 地精女儿 · 剧情02 | 14 | GoblinDaughterWoods3 |
| 489 | 地精女儿 · 剧情03 | 13 | GoblinDaughterWoods4 |
| 496 | 骑士袭击 | 89 | GoblinHallBedroom |
| 497 | Shakala · GD H01 | 89 | GoblinHallBedroom |
| 653 | Erevi · 黑色礼服（灵药） | 8 | KitchenTOD |
| 1250 | 女儿 · 巨魔 | 34 | TODPlay, TODPlayNP |
| 1251 | 女儿 · 地牢玩具 | 52 | TODSexToy, TODSexToyPreg |
| 1254 | 女儿 · 王子 | 34 | TODPlay, TODPlayHU, TODPlayHUNP |
| 1491 | Qetesh · 喷泉 | 19 | TempleFountain2C, TempleFountainC |
| 1498 | 地牢装置 · ED | 32 | DDED, DDED_P |
| 1556 | Beth · 求欢1（大场景） | 56 | StablesN3, StablesN3P, StablesN4 |
| 1644 | ED · 湿身少女 | 26 | EDMoistMaiden, EDMoistMaidenBT |
| 1783 | ED · 脱衣 | 9 | EDMoistMaiden, EDPleasure, EDStripB2 |
| 1823 | ED · 课程 | 42 | EDLessonsX, EDLessonsXBT, EDLessonsXP |
| 1829 | Qetesh · 床上 | 17 | Apparition3, Apparition3C |
| 1833 | Erevi · 新婚夜 ED | 58 | EWNX, EWNX1, EWNXP |
| 1837 | Qetesh · 宫殿1 | 30 | PalaceOfQeteshX, PalaceOfQeteshX1, PalaceOfQeteshX1P |
| 1838 | Qetesh · 宫殿2 | 30 | PalaceOfQeteshX2, PalaceOfQeteshX2P, PalaceOfQeteshX3 |

## 参数说明

| 参数 | 本作取值 | 说明 |
|---|---|---|
| `sceneList` | 306 项 | 场景列表，`[id, 中文名, 英文原名]` |
| `openKey` | `118`（F7） | 打开列表 |
| `nextKey` | `119`（F8） | 播放下一个 |
| `autoKey` | `120`（F9） | 自动连播开关 |
| `msgKey` | `121`（F10） | 自动推进对话开关 |
| `autoDelay` | `60` | 场景结束后等多少帧播下一个（60 帧 ≈ 1 秒） |
| `msgDelay` | `45` | 对话显示完后等多少帧翻页（45 帧 ≈ 0.75 秒） |
| `missingAssets` | 30 个场景 | 缺素材清单 `{"场景id":["图片名",...]}` |

常用 keyCode：F6=117、F7=118、F8=119、F9=120、F10=121、F11=122。

> 若按 `F7` 出现怪异光标（Chromium 的「插入符浏览」抢键），把 `openKey` 改成 `"117"`（F6）。

---

## 仓库内容

```
ScenePlayer.js              插件本体（638 行，无构建步骤）
SCENES.md                   306 个场景对照表（id / 中文名 / 原名 / 指令数 / 缺素材 / 是否在 unlockEvents）
params/sceneList.json       306 项场景列表（可读格式）
params/missingAssets.json   30 个缺素材场景的 884 个缺失文件名
params/names.zh.json        {场景id: 中文名}（306 条），供重新生成时复用
params/plugins-entry.txt    可直接粘进 www/js/plugins.js 的整行条目
tools/scan_game.py          扫描游戏重新生成上面这些参数
tools/fix-unlock-events.py   修正作弊菜单的 unlockEvents（剔除缺素材 id / 装包后恢复）
CHANGELOG.md                更新日志
```

## 重新生成清单（游戏更新到 NYD413+ 时）

```bash
# 一条命令全自动：扫描 → 生成参数 → 写入 plugins.js → 修正 unlockEvents
python3 tools/setup.py "/path/to/农民的任务" --rebuild-unlock --yes

# 只想拿到参数文本：
python3 tools/scan_game.py "/path/to/农民的任务/www" --mode auto \
    --names params/names.zh.json --exclude 410,411,1894,1895,1896 \
    --emit entry > params/plugins-entry.txt
```

脚本沿「调用公共事件」（指令 117）**递归**收集图片，因此被场景调用的子事件缺图也能算出来。`--exclude` 里的 5 个是本作真正非 CG 的（系统过场 + 精灵动画机位子事件）。

> 注意：`--names` 只对新 id 之外的部分生效；如果新版本改动了场景名，中文名映射需要手工补。

## 常见问题

**Q：按 F8 没反应，或者弹出了开发者工具？**
本作因为 `ListenToF8.js` 改过 `SceneManager.onKeyDown`，F8 是空的，正常可用。若你装了别的改键插件导致冲突，把 `nextKey` 改成 `"117"`（F6）或 `"122"`（F11）。

**Q：报 `Loading Error: Failed to load: img/pictures/...`？**
说明素材缺失。本作那 30 个已在 `missingAssets` 里，插件会拦住；如果报了**新的**文件，说明游戏更新了或装了一半内容包，重新跑一遍 `tools/scan_game.py` 更新 `missingAssets` 即可。

**Q：报 `TypeError: Cannot read property 'length' of undefined` at `maxItems`？**
v1.0.0 的 bug（`Window_Selectable.initialize` 内部会先调 `maxItems()`，而当时 `_data` 还没初始化），v1.0.1 已修，请用最新版。

**Q：作弊菜单里选到缺素材的场景照样报错？**
对，`VirtualacgPC` 的 `unlockEvents` 里也含这 30 个 id，那个菜单不走本插件的素材检查，选到就是 `Loading Error`。

推荐把 `unlockEvents` 收窄到 **276 个**（`306 - 30`），仓库里的脚本可以直接做：

```bash
# 先看会改什么
python3 tools/fix-unlock-events.py "/path/to/农民的任务/www" --dry-run
# 执行（自动备份 plugins.js.bak-<时间戳>，改完回读校验）
python3 tools/fix-unlock-events.py "/path/to/农民的任务/www"
# 以后装了 Spicy Mod，一键把 306 个全加回来
python3 tools/fix-unlock-events.py "/path/to/农民的任务/www" --restore
```

脚本默认从 `ScenePlayer.missingAssets` 读取要剔除的 id（没装 ScenePlayer 时用 `--drop` 指定），可重复执行（幂等）。

于是两个入口的分工是刻意的：

- **ScenePlayer 列表（F7）**：306 个全列出，缺素材的标 ⚠ 并在播放/连播时跳过 —— 让你知道有哪些场景存在；
- **作弊菜单「解锁公共事件」**：276 个，不含缺素材场景 —— 因为那个菜单没有素材检查能力。

**Q：自动连播到某个场景停了？**
① 该场景缺素材被跳过、且后面没有可播的了 → 插件会提示「自动连播已停止」；② 场景里有需要你操作的选项 —— `F10` 的自动推进**不会替你选选项**，这是刻意设计。

**Q：会污染存档吗？**
插件本身只调 `$gameTemp.reserveCommonEvent(id)`，不写存档。但**被触发的场景本身会改开关/变量/物品**，按顺序乱播 306 个场景可能把进度搞乱。**建议先存一个独立存档再玩自动连播。**

**Q：怎么彻底回滚？**
本仓库不含游戏文件。删插件文件 + 删 `plugins.js` 里那条即可，游戏本体不受影响。

## 开发与测试

插件是单文件、无构建步骤。核心逻辑（列表解析、缺素材判定、连播推进、跳过、按键路由）都是 `ScenePlayer.*` 上的纯方法，可以在 Node 里用最小 MV 运行时桩做无头测试，不必启动游戏。

写测试桩时**务必忠实复刻** `Window_Selectable.prototype.initialize` 那条调用链：
`initialize → deactivate → reselect → select → ensureCursorVisible → maxTopRow → maxRows → maxItems`。
v1.0.0 那个崩溃就是因为测试桩简化了这条链而漏掉的。

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)。

## License

[MIT](LICENSE)。本仓库只含插件代码与场景清单（id/名称），**不含任何游戏资源**。
