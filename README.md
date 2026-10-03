# ScenePlayer — RPG Maker MV 场景速播器

给 RPG Maker MV 游戏用的「公共事件（场景）速播器」。不用再在游戏菜单里一个个点，直接用一个键连着看、或者全自动连播。

适用于任何 MV 游戏：你给它一份「场景列表」，它就给你一个**键盘驱动的场景浏览器** + **单键推进** + **自动连播** + **自动推进对话**，并且会**预检素材是否存在**，避免播到缺图的场景把游戏打成 `Loading Error`。

> 例：某游戏的 162 个剧情/CG 场景，配上中文名后在列表里是这样显示的
> ```
>    19  #295  女儿 · 床上1  ⚠缺素材
>               缺 23 张图，需 Spicy Mod：DaughterBedScene - 001
>    20  #340  Liandra · H2
>               LiandraSexScene2
> ```

---

## 功能

| 功能 | 说明 |
|---|---|
| **F7 场景列表** | 键盘驱动的列表窗：翻页、跳转、直接播放选中项；每项两行显示（自定义名 + 原始事件名） |
| **F8 单键下一个** | 不开任何菜单，按一下播下一个场景；连按就是连着看 |
| **F9 自动连播** | 当前场景一结束，自动接下一个（间隔可配） |
| **F10 自动推进对话** | 对话显示完整后自动翻页；**遇到选项/数字输入绝不替你选** |
| **缺素材检测** | 启动时读取 `img/pictures` 建立索引，缺图的场景标红 ⚠、拒绝播放、自动连播时跳过 |
| **控制台 API** | `ScenePlayer.playId(1257)` 之类，方便脚本化调试 |

设计上刻意保守：

- 只做「触发公共事件」，**不直接改存档数据**（但被触发的场景本身可能会改开关/变量，见下文注意事项）。
- 事件/对话正在运行时不会重入，避免叠事件。
- 探测不到素材目录时退回离线标记，不会把所有场景误判成缺失。

---

## 适用环境

- **RPG Maker MV**（`RPGMAKER_NAME === 'MV'`），NW.js 桌面版或浏览器版均可。
- 缺素材检测依赖 NW.js 的 `require('fs')`；浏览器版会自动退回离线清单。
- 与 `YEP_*`、`SRD_SuperToolsEngine`、`Galv_*` 等常见插件共存（会正确调用被覆盖的 `Window_Selectable.initialize`）。

> 注意：本插件是 MV 版。MZ 的窗口类/`Window_Selectable` 接口有差异，未做适配。

---

## 安装

### 1. 放入插件文件

把 `ScenePlayer.js` 复制到游戏的插件目录：

```
<游戏目录>/js/plugins/ScenePlayer.js
```

### 2. 在 `js/plugins.js` 注册

打开 `<游戏目录>/js/plugins.js`，在 `var $plugins = [ ... ]` 数组**末尾**加一条（放在最后可以确保钩子在其它插件之后生效）：

```js
{"name":"ScenePlayer","status":true,"description":"场景速播器","parameters":{
  "sceneList":"[[10,\"Ziva · 剧情01\",\"ZivaScene01\"],[340,\"Liandra · H2\",\"LiandraSexScene2\"]]",
  "openKey":"118","nextKey":"119","autoKey":"120","msgKey":"121",
  "autoDelay":"60","msgDelay":"45","missingAssets":"{}"
}},
```

⚠️ 两个易错点：

- `plugins.js` 里所有参数值**必须是字符串**（`"118"` 而不是 `118`），里面的 JSON 要再转义一层引号。
- 数组元素之间记得加逗号，别破坏原有条目的结构。改完可以先 `node --check js/plugins.js` 验一下语法。

### 3. 生成 `sceneList`

`sceneList` 就是你要播的公共事件列表，格式：

```jsonc
[
  [10,  "显示名", "原始事件名"],   // 三元组：id、自定义名（可中文）、原名（显示在第二行）
  [340, "Liandra · H2"],          // 二元组：不显示第二行
  [2001]                          // 一元组：只给 id，显示为 #2001
]
```

两种生成方式：

**A. 用附带的扫描脚本（推荐）** —— 见下文「`tools/scan_game.py`」，它会扫 `data/CommonEvents.json` 自动列出候选场景，并把缺素材清单一起算好。

**B. 手写** —— 打开 RPG Maker MV 编辑器看公共事件 id，或直接读 `data/CommonEvents.json`。

### 4. 重启游戏

MV 在启动时加载插件，改完必须重启游戏（`F5` 或关掉重开）才生效。

---

## 参数说明

| 参数 | 默认 | 说明 |
|---|---|---|
| `sceneList` | `[]` | 场景列表，JSON 数组。支持 `[id]` / `[id, 名称]` / `[id, 名称, 原名]`。留空则快捷键无效 |
| `openKey` | `118` | 打开列表的按键 keyCode（118 = F7） |
| `nextKey` | `119` | 播放下一个（119 = F8） |
| `autoKey` | `120` | 自动连播开关（120 = F9） |
| `msgKey` | `121` | 自动推进对话开关（121 = F10） |
| `autoDelay` | `60` | 一个场景结束后等多少帧播下一个（60 帧 ≈ 1 秒） |
| `msgDelay` | `45` | 对话显示完后等多少帧自动翻页（45 帧 ≈ 0.75 秒） |
| `missingAssets` | `{}` | 缺素材清单 `{"场景id":["图片名", ...]}`。列表标 ⚠、自动连播跳过；NW.js 下会**实时复核**，素材补上就自动放行 |

### 常用 keyCode

| 键 | keyCode | 键 | keyCode |
|---|---|---|---|
| F6 | 117 | F9 | 120 |
| F7 | 118 | F10 | 121 |
| F8 | 119 | F11 | 122 |

> **F7 在 Chromium 里是「插入符浏览」**，个别版本会抢键。如果按 F7 没反应或出现怪异光标，把 `openKey` 改成 `"117"`（F6）即可。
>
> **F8 在标准 MV 里是「打开开发者工具」**（仅 test 模式）。有些游戏用 `SceneManager.onKeyDown` 把它改掉了，这时 F8 可安全使用；没改的游戏里按 F8 会弹出 devtools，把 `nextKey` 改成 `"117"`（F6）或 `"122"`（F11）即可。

---

## 使用方法

### 游戏内快捷键（场景地图上生效）

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

列表第一行是自定义名（选中＝蓝、上次播放＝橙、缺素材＝红 + ⚠），第二行是原始事件名（小字半透明）。

### 控制台 API

游戏里按 `F12`（Chromium 默认）打开开发者工具，在 Console 里：

```js
ScenePlayer.playNext()        // 播放下一个
ScenePlayer.playPrev()        // 播放上一个
ScenePlayer.play(67)          // 播放列表第 68 项（0 起）
ScenePlayer.playId(1257)      // 按公共事件 id 播放（不在列表里也能播）
ScenePlayer.toggleAuto()      // 切换自动连播
ScenePlayer.toggleMsgAuto()   // 切换自动推进对话
ScenePlayer.status()          // 打印当前状态
ScenePlayer.checkAssets()     // 打印缺素材报告
ScenePlayer.scenes            // 当前场景列表（含 id / name / orig）
```

---

## 缺素材检测（`missingAssets`）

### 为什么需要

很多 MV 游戏有「可选内容包」（额外剧情/CG），没装的话对应图片文件不存在。一旦触发那些场景，MV 会抛出：

```
Loading Error
Failed to load: img/pictures/XXX.png
```

游戏直接卡在报错画面，`Retry` 也没用（文件本来就不存在）。

### 它怎么工作

1. 启动后**首次需要时**（不是开机时）读取 `img/pictures` 目录，建立文件名索引；
2. 先用一张必然存在的通用图（`BlackImage`）自检目录是否找对了，`www/img/pictures/` 和 `img/pictures/` 两种布局都会尝试；找不到就退回离线清单；
3. 检查 `missingAssets` 里列出的文件名，**只有确实缺失的才拦**；
4. 于是：**素材补上后自动放行**，不用改配置。

### 怎么生成

用 `tools/scan_game.py`（见下），或者手写：

```json
{"295":["DaughterBedScene - 001","DaughterBedScene - 101"],"1251":["TODSexToy - 001"]}
```

---

## `tools/scan_game.py`

扫描一个 MV 游戏，自动生成 `sceneList` 和 `missingAssets` 参数。

```bash
python3 tools/scan_game.py /path/to/game/www
```

- 默认按事件名里含 `scene`（不区分大小写）挑选候选场景；
- 只挑「有实际指令」的事件，跳过空壳和纯注释事件；
- 会沿「调用公共事件」（指令 117）**递归**收集图片，所以被场景调用的子事件缺图也能算出来；
- 检查 `img/pictures` 下 `.rpgmvp/.png/.jpg/.jpeg/.webp`，输出缺素材清单。

常用选项：

```bash
# 换个匹配规则
python3 tools/scan_game.py /path/to/game/www --pattern "cg|scene"

# 排除掉不想要的 id（比如系统过场）
python3 tools/scan_game.py /path/to/game/www --exclude 410,411,487

# 给指定 id 加中文名
python3 tools/scan_game.py /path/to/game/www --names names.json
# names.json: {"10":"Ziva · 剧情01","340":"Liandra · H2"}

# 直接输出可粘进 plugins.js 的完整条目
python3 tools/scan_game.py /path/to/game/www --emit entry
```

---

## 常见问题

**Q：按 F7/F8 没反应，或者按 F8 弹出了开发者工具？**
确认插件已注册且 `"status":true`，并重启过游戏。按键被系统/引擎占用时改对应参数即可：F7 → `openKey:"117"`（F6），F8 → `nextKey:"117"` 或 `"122"`（F11），见上文 keyCode 表。另外快捷键只在**场景地图**上生效（菜单/战斗中不响应）。

**Q：报 `Loading Error: Failed to load: img/pictures/...`？**
这就是缺素材，用 `tools/scan_game.py` 生成 `missingAssets` 填进去；或者干脆把那些场景从 `sceneList` 里删掉。补上素材后不需要改配置。

**Q：报 `TypeError: Cannot read property 'length' of undefined` 在 `maxItems`？**
那是 v1.0.0 的 bug，`Window_Selectable.initialize` 内部会调 `maxItems()`，而 `_data` 当时还没初始化。v1.0.1 已修（先初始化再调父类），请更新到最新版。

**Q：自动连播到某个场景就停了？**
两种可能：① 该场景缺素材被跳过，但后面也没有可播的了 → 插件会提示「自动连播已停止（没有可播放的场景）」；② 场景里有需要你操作的选项 —— `F10` 的自动推进**不会替你选选项**，这是刻意设计。

**Q：会不会污染存档？**
插件本身只调用 `$gameTemp.reserveCommonEvent(id)`，不写存档。但**被触发的场景本身可能会改开关/变量/物品**（尤其是按顺序乱播时）。建议先存一个独立存档再玩自动连播。

**Q：怎么彻底卸载？**
删掉 `js/plugins/ScenePlayer.js`，并把 `js/plugins.js` 里 `"name":"ScenePlayer"` 那条删掉（或把 `"status"` 改成 `false` 临时禁用）。

**Q：列表里显示的是原始事件名，看不懂？**
在 `sceneList` 里给每一项补第二元素作为显示名即可，例如 `[1257,"Victoria×Gwynneth · H（大场景）","SexSceneVictoriaGwynneth"]`。

---

## 开发与测试

插件是单文件、无构建步骤。核心逻辑（场景列表解析、缺素材判定、连播推进、跳过逻辑、按键路由）都做成了纯函数式的 `ScenePlayer.*` 方法，可以在 Node 里用最小 MV 运行时桩做无头测试——不需要启动游戏。

写测试桩时**务必忠实复刻** `Window_Selectable.prototype.initialize` 那条调用链（`initialize → deactivate → reselect → select → ensureCursorVisible → maxTopRow → maxRows → maxItems`）。v1.0.0 那个崩溃就是因为测试桩简化了这条链而漏掉的。

## 更新日志

见 [CHANGELOG.md](CHANGELOG.md)。

## License

[MIT](LICENSE)
