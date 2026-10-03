# 更新日志

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
