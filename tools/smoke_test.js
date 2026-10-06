#!/usr/bin/env node
/**
 * ScenePlayer 无头冒烟测试。
 *
 * 用最小 MV 运行时桩加载**游戏里实际安装的** ScenePlayer.js（不是仓库副本），
 * 所以它验证的是「真正跑起来的那份代码」。无需启动游戏。
 *
 * 用法：
 *   node tools/smoke_test.js                      # 默认测本作路径
 *   node tools/smoke_test.js /path/to/game        # 指定游戏根目录
 *
 * 写桩时的注意事项（踩过坑）：
 *   1. Window_Selectable.prototype.initialize 必须逐行复刻 MV 的调用链
 *      initialize → deactivate → reselect → select → ensureCursorVisible
 *      → maxTopRow → maxRows → maxItems
 *      （v1.0.0 的崩溃就是因为桩简化了这条链而漏掉的）
 *   2. Game_Event.list() 要按 MV 原样实现为 this.page().list
 *      （没有任何事件页条件满足时 page() 是 undefined，会抛错）
 */

'use strict';
const fs = require('fs');
const path = require('path');

const GAME = (process.argv[2] || '/mnt/d/Downloads/h/PC Peasants Quest NYD412').replace(/\/+$/, '');
const PLUGIN = path.join(GAME, 'www/js/plugins/ScenePlayer.js');
const PLUGINS_JS = path.join(GAME, 'www/js/plugins.js');
if (!fs.existsSync(PLUGIN) || !fs.existsSync(PLUGINS_JS)) {
    console.error('找不到 ' + PLUGIN + ' 或 ' + PLUGINS_JS);
    process.exit(2);
}

// ---- 从真实 plugins.js 取参数 ----
const pjs = fs.readFileSync(PLUGINS_JS, 'utf8');
const entries = JSON.parse(pjs.match(/var \$plugins\s*=\s*(\[[\s\S]*\]);/)[1]);
const spEntry = entries.find(e => e.name === 'ScenePlayer');
if (!spEntry) { console.error('plugins.js 里没有 ScenePlayer 条目'); process.exit(2); }
const params = spEntry.parameters;
const P_SCENES = JSON.parse(params.sceneList);
const P_MAPS = JSON.parse(params.mapScenes || '[]');
const P_MISS = JSON.parse(params.missingAssets);
const P_TAGS = JSON.parse(params.tags || '{}');
const P_SUBS = JSON.parse(params.subScenes || '{}');

// ---- MV 运行时桩 ----
Number.prototype.clamp = function (min, max) { return Math.min(Math.max(this, min), max); };
global.window = global;
global.addEventListener = () => {};
global.Graphics = { boxWidth: 1008, boxHeight: 720 };
global.PluginManager = { parameters: () => params };

function Window_Base() {}
Window_Base.prototype.initialize = function (x, y, w, h) {
    this.x = x; this.y = y; this.width = w; this.height = h; this.padding = 18;
    this.contents = { fontSize: 28, paintOpacity: 255, clear() {} };
};
Window_Base.prototype.update = function () {};
Window_Base.prototype.fittingHeight = n => 36 * (n || 1);
Window_Base.prototype.lineHeight = () => 36;
Window_Base.prototype.standardFontSize = () => 28;
Window_Base.prototype.linePadding = () => 4;
Window_Base.prototype.changeTextColor = function (c) { this._color = c; };
Window_Base.prototype.resetTextColor = function () { this._color = null; };
Window_Base.prototype.powerUpColor = () => 'orange';
Window_Base.prototype.systemColor = () => 'blue';
Window_Base.prototype.deathColor = () => 'red';
Window_Base.prototype.itemRectForText = i => ({ x: 0, y: i * 72, width: 900, height: 72 });
Window_Base.prototype.drawText = function (t, x, y, w) {
    (this._drawn = this._drawn || []).push({ t, y, size: this.contents.fontSize, opa: this.contents.paintOpacity });
};
Window_Base.prototype.activate = function () { this.active = true; };
Window_Base.prototype.deactivate = function () { this.active = false; };

function Window_Selectable() {}
Window_Selectable.prototype = Object.create(Window_Base.prototype);
Window_Selectable.prototype.constructor = Window_Selectable;
Window_Selectable.prototype.initialize = function (x, y, w, h) {
    Window_Base.prototype.initialize.call(this, x, y, w, h);
    this._index = -1; this._cursorFixed = false; this._cursorAll = false;
    this._stayCount = 0; this._helpWindow = null; this._handlers = {};
    this._touching = false; this._scrollX = 0; this._scrollY = 0;
    this.deactivate();
};
Window_Selectable.prototype.update = function () {};
Window_Selectable.prototype.processCursorMove = function () {};
Window_Selectable.prototype.isCursorMovable = () => false;
Window_Selectable.prototype.index = function () { return this._index; };
Window_Selectable.prototype.maxCols = () => 1;
Window_Selectable.prototype.maxItems = () => 0;
Window_Selectable.prototype.itemHeight = function () { return this.lineHeight(); };
Window_Selectable.prototype.row = function () { return Math.floor(this.index() / this.maxCols()); };
Window_Selectable.prototype.topRow = function () { return Math.floor(this._scrollY / this.itemHeight()); };
Window_Selectable.prototype.maxPageRows = function () { return Math.floor((this.height - this.padding * 2) / this.itemHeight()); };
Window_Selectable.prototype.maxRows = function () { return Math.max(Math.ceil(this.maxItems() / this.maxCols()), 1); };
Window_Selectable.prototype.maxTopRow = function () { return Math.max(0, this.maxRows() - this.maxPageRows()); };
Window_Selectable.prototype.bottomRow = function () { return this.topRow() + this.maxPageRows() - 1; };
Window_Selectable.prototype.setTopRow = function (row) {
    var scrollY = row.clamp(0, this.maxTopRow()) * this.itemHeight();
    if (this._scrollY !== scrollY) { this._scrollY = scrollY; this.refresh(); this.updateCursor(); }
};
Window_Selectable.prototype.setBottomRow = function (row) { this.setTopRow(row - (this.maxPageRows() - 1)); };
Window_Selectable.prototype.ensureCursorVisible = function () {
    var row = this.row();
    if (row < this.topRow()) this.setTopRow(row);
    else if (row > this.bottomRow()) this.setBottomRow(row);
};
Window_Selectable.prototype.select = function (i) {
    this._index = i; this._stayCount = 0; this.ensureCursorVisible();
    this.updateCursor(); this.callUpdateHelp();
};
Window_Selectable.prototype.reselect = function () { this.select(this._index); };
Window_Selectable.prototype.deactivate = function () { Window_Base.prototype.deactivate.call(this); this.reselect(); };
Window_Selectable.prototype.activate = function () { Window_Base.prototype.activate.call(this); this.reselect(); };
Window_Selectable.prototype.updateCursor = function () {};
Window_Selectable.prototype.callUpdateHelp = function () { this.updateHelp(); };
Window_Selectable.prototype.refresh = function () {};
Window_Selectable.prototype.setHandler = function (k, f) { (this._handlers = this._handlers || {})[k] = f; };

function Window_Help() {}
Window_Help.prototype = Object.create(Window_Base.prototype);
Window_Help.prototype.initialize = function () { Window_Base.prototype.initialize.call(this, 0, 0, 1008, 72); };
Window_Help.prototype.setText = function (t) { this._text = t; };

function Scene_Base() {}
Scene_Base.prototype.create = function () {};
Scene_Base.prototype.popScene = function () { popped = true; };
Scene_Base.prototype.addWindow = function (w) { (this._windows = this._windows || []).push(w); };
function Scene_MenuBase() {}
Scene_MenuBase.prototype = Object.create(Scene_Base.prototype);
Scene_MenuBase.prototype.constructor = Scene_MenuBase;
Scene_MenuBase.prototype.create = function () {};
Scene_MenuBase.prototype.update = function () {};
function Scene_Map() {}
Scene_Map.prototype = Object.create(Scene_Base.prototype);
Scene_Map.prototype.constructor = Scene_Map;
Scene_Map.prototype.createAllWindows = function () {};
Scene_Map.prototype.update = function () { this.updated = (this.updated || 0) + 1; };

Object.assign(global, { Window_Base, Window_Selectable, Window_Help, Scene_Base, Scene_MenuBase, Scene_Map });
global.Utils = { isNwjs: () => false };
global.Input = { keyMapper: {}, isRepeated: () => false, isTriggered: () => false };
global.SceneManager = { _scene: null, isSceneChanging: () => false, push: () => { pushed = true; } };
global.TouchInput = { isCancelled: () => false };

let reserved = [], pushed = false, popped = false, transferred = [];
let msgBusy = false, evRunning = false, mapId = 1, transferring = false;
const fakeEvents = {};
global.$gameTemp = { reserveCommonEvent: id => reserved.push(id) };
global.$gameMessage = { isBusy: () => msgBusy, clear: () => { msgBusy = false; } };
global.$gamePlayer = {
    isTransferring: () => transferring,
    reserveTransfer: (m, x, y, d, f) => { transferred.push([m, x, y]); }
};
global.$gameMap = {
    mapId: () => mapId,
    isEventRunning: () => evRunning,
    event: id => fakeEvents[id] || null
};

// ---- 抓取插件内部类原型 ----
let Window_SceneListProto = null, Scene_ScenePlayerProto = null;
const _oc = Object.create.bind(Object);
Object.create = function (proto, props) {
    const o = _oc(proto, props);
    if (proto === Window_Selectable.prototype) Window_SceneListProto = o;
    if (proto === Scene_MenuBase.prototype) Scene_ScenePlayerProto = o;
    return o;
};
require(PLUGIN);
Object.create = _oc;
const SP = global.ScenePlayer;

let pass = 0, fail = 0;
const ok = (c, m) => { c ? pass++ : fail++; console.log((c ? '  ✅ ' : '  ❌ ') + m); };
const idx = (kind, id) => SP.view.findIndex(it => it.kind === kind && (kind === 'ce' ? it.id === id : it.key === id));
const reset = () => { reserved = []; transferred = []; pushed = false; popped = false; evRunning = false; msgBusy = false; transferring = false; };

console.log('== 加载与解析 ==');
ok(SP.items.length === P_SCENES.length + P_MAPS.length,
   'items = ' + SP.items.length + '（公共事件 ' + P_SCENES.length + ' + 地图 ' + P_MAPS.length + '）');
ok(SP.scenes.length === P_SCENES.length && SP.mapScenes.length === P_MAPS.length, 'SP.scenes / SP.mapScenes 数量正确');
ok(SP.showSub === false, '默认隐藏子场景');
ok(SP.view.length === SP.items.length - Object.keys(P_SUBS).length,
   '默认列表 = ' + SP.view.length + '（' + SP.items.length + ' − ' + Object.keys(P_SUBS).length + ' 个子场景）');
SP.showSub = true; SP.applyFilter();      // 以下「全表」断言都在显示子场景的状态下做
ok(SP.view.length === SP.items.length, '显示子场景后 view = items = ' + SP.view.length);
ok(SP.items.filter(i => i.kind === 'map').length === P_MAPS.length, '地图场景已并入 items');
ok(!!Window_SceneListProto && !!Scene_ScenePlayerProto, '内部窗口/画面类已注册');

console.log('== 类型标签 ==');
const cnt = t => SP.items.filter(i => i.tag === t).length;
ok(SP.countByTag('h') === cnt('h') && cnt('h') > 0, 'H 标签 ' + cnt('h') + ' 个');
ok(cnt('story') > 0 && cnt('misc') > 0, '剧情 ' + cnt('story') + ' / 杂项 ' + cnt('misc'));
ok(SP.items.every(i => ['h', 'story', 'misc'].indexOf(i.tag) >= 0), '每个场景都有合法标签');
ok(SP.itemOf(0).key === String(P_SCENES[0][0]), '首项 key = ' + SP.itemOf(0).key);

console.log('== 筛选切换 ==');
SP.setFilter('h');
ok(SP.view.length === cnt('h') && SP.view.every(i => i.tag === 'h'), '仅H -> ' + SP.view.length);
SP.setFilter('story');
ok(SP.view.length === cnt('story'), '仅剧情 -> ' + SP.view.length);
SP.setFilter('misc');
ok(SP.view.length === cnt('misc'), '仅杂项 -> ' + SP.view.length);
SP.setFilter('all');
ok(SP.view.length === SP.items.length, '切回全部');
const firstH = SP.items.findIndex(i => i.tag === 'h');
SP.setFilter('all'); SP.lastKey = SP.items[firstH].key;
SP.setFilter('h');
ok(SP.last >= 0 && SP.view[SP.last].key === SP.items[firstH].key, '切换筛选后 last 按 lastKey 重定位');
SP.cycleFilter();
ok(SP.filter === 'story', 'cycleFilter 从 h 轮到 story（实际 ' + SP.filter + '）');
SP.setFilter('all');

console.log('== 子场景（嵌套）==');
const SUB_KEYS = Object.keys(P_SUBS);
ok(SUB_KEYS.length > 0, '参数里有 ' + SUB_KEYS.length + ' 个子场景');
ok(SP.countSub() === SUB_KEYS.length, 'countSub() = ' + SP.countSub());
ok(SP.showSub === true, '（本节开始时为显示态）');
SP.toggleSub();
ok(SP.showSub === false, 'F4 -> 隐藏子场景');
ok(SP.view.length === SP.items.length - SUB_KEYS.length,
   '隐藏后列表 = ' + SP.view.length + '（' + SP.items.length + ' − ' + SUB_KEYS.length + '）');
ok(SP.view.every(i => !i.subOf), '隐藏后列表里没有子场景');
SP.toggleSub();
ok(SP.showSub === true && SP.view.length === SP.items.length, 'F4 再按 -> 恢复显示全部');
const subKey0 = SUB_KEYS[0];
const subItem = SP.items.find(i => i.key === subKey0);
ok(!!subItem && !!subItem.subOf && subItem.subOf.length === P_SUBS[subKey0].length,
   '子场景 #' + subKey0 + ' 记录了 ' + (subItem ? subItem.subOf.length : 0) + ' 个调用者');
ok(subItem.subOf.every(c => SP.items.some(i => i.key === String(c))),
   '调用者键都能解析到场景（' + subItem.subOf.slice(0, 2).join(', ') + '）');
ok(SP.nameOfKey(subItem.subOf[0]) !== '#' + subItem.subOf[0],
   'nameOfKey 能查到调用者名字: ' + SP.nameOfKey(subItem.subOf[0]));
// 环保护：互相调用且无环外入口的一组，必须留一个可见
const cyc = SP.items.filter(i => i.subOf && i.subOf.some(c => SP.items.find(j => j.key === String(c) && j.subOf && j.subOf.indexOf(Number(i.key)) >= 0)));
const cycVisible = cyc.filter(i => !i.subOf);
ok(cyc.length > 0 ? cycVisible.length > 0 : true,
   '互相调用的环里至少有一个可见入口（环内 ' + cyc.length + ' 个）');
// 与标签筛选叠加
SP.setFilter('h');
ok(SP.view.every(i => i.tag === 'h'), '显示子场景时标签筛选仍生效');
SP.toggleSub();
ok(SP.showSub === false && SP.view.every(i => i.tag === 'h' && !i.subOf),
   '隐藏子场景 + 仅H 同时生效（' + SP.view.length + ' 项）');
SP.toggleSub();
SP.setFilter('all');
ok(SP.showSub === true && SP.view.length === SP.items.length, '恢复全表');

console.log('== 缺素材（含影片）==');
const missKeys = Object.keys(P_MISS);
const movKeys = missKeys.filter(k => P_MISS[k].some(x => x.startsWith('movie:')));
ok(missKeys.length > 0, '参数里有 ' + missKeys.length + ' 个缺素材场景');
ok(movKeys.length > 0, '其中 ' + movKeys.length + ' 个含缺失影片');
const i295 = idx('ce', 295);
ok(i295 >= 0 && SP.missingOf(i295).length === P_MISS['295'].length,
   '#295 缺 ' + SP.missingOf(i295).length + ' 项（参数 ' + P_MISS['295'].length + '）');
ok(SP.canPlay(i295) === false, '#295 不可播');
const movScene = idx('ce', parseInt(movKeys[0], 10));
ok(SP.missingOf(movScene).some(x => x.startsWith('movie:')),
   '影片缺失被识别: ' + SP.missingOf(movScene).filter(x => x.startsWith('movie:'))[0]);
ok(SP.assetMissing('movie:随便一个不存在的影片') === true, 'assetMissing 对未知影片返回 true');
ok(SP.view.findIndex(i => SP.canPlay(i)) >= 0, '存在可播场景');
let blocked = 0;
for (let i = 0; i < SP.view.length; i++) if (!SP.canPlay(i)) blocked++;
ok(blocked === missKeys.length, '整表缺素材场景 = ' + blocked + '（参数 ' + missKeys.length + '）');
// 地图场景的缺素材键（m<mapId>:<eventId>）也必须生效
const mapMissKey = missKeys.find(k => k.startsWith('m'));
if (mapMissKey) {
    const pos = SP.view.findIndex(i => i.key === mapMissKey);
    ok(pos >= 0 && SP.missingOf(pos).length === P_MISS[mapMissKey].length,
       '地图场景缺素材键生效（' + mapMissKey + ' 缺 ' + SP.missingOf(pos).length + ' 项）');
} else {
    ok(true, '（本次参数里没有缺素材的地图场景）');
}

console.log('== 播放公共事件 ==');
reset();
const posCE = idx('ce', P_SCENES[0][0]);
ok(SP.play(posCE) === true, 'play(公共事件) = true');
ok(reserved[0] === P_SCENES[0][0], 'reserveCommonEvent(' + reserved[0] + ')');
ok(SP.last === posCE && SP.lastKey === String(P_SCENES[0][0]), 'last/lastKey 已更新');
ok(SP.playing === true, 'playing = true');
reset();
ok(SP.play(i295) === false && reserved.length === 0, '缺素材场景被拒绝且不触发事件');

console.log('== 播放地图场景（同一张地图）==');
reset();
const mapItem = P_MAPS[0];
const posMap = idx('map', 'm' + mapItem[0] + ':' + mapItem[1]);
let started = 0;
const mkEvent = (list, starting) => {
    const ev = { isStarting: () => !!starting, start: () => { started++; } };
    ev.page = () => (list ? { list: list } : undefined);   // _pageIndex=-1 时是 undefined
    ev.list = function () { return this.page().list; };      // 与 rpg_objects.js 一致
    return ev;
};
fakeEvents[mapItem[1]] = mkEvent([{ code: 0 }, { code: 401 }], false);
mapId = mapItem[0];
ok(SP.play(posMap) === true, 'play(地图场景) = true');
ok(started === 1, '调用了 event.start() 一次');
ok(transferred.length === 0, '同地图不传送');
ok(SP.playing === true && SP.pending === null, 'playing=true，无 pending');

console.log('== 播放地图场景（需要传送）==');
reset();
started = 0; mapId = 999;
ok(SP.play(posMap) === true, 'play 返回 true');
ok(transferred.length === 1 && transferred[0][0] === mapItem[0], '触发了 reserveTransfer 到 Map' + transferred[0][0]);
ok(SP.pending !== null && started === 0, '先挂 pending，尚未触发事件');
transferring = true; SP.update();
ok(started === 0, '传送中不触发');
transferring = false; mapId = mapItem[0]; SP.update();
ok(started === 1, '落地后触发事件');
ok(SP.pending === null, 'pending 已清空');
reset(); started = 0; mapId = 999;
SP.play(posMap);
SP.pendingWait = 2;
SP.update(); SP.update(); SP.update();
ok(SP.pending === null && SP.playing === false, '传送超时会放弃并复位');
ok(started === 0, '超时不会触发事件');

console.log('== startMapEvent 边界 ==');
reset(); mapId = mapItem[0];
delete fakeEvents[mapItem[1]];
SP.play(posMap);
ok(SP.playing === false, '事件不存在 -> 不进入播放态');
fakeEvents[mapItem[1]] = mkEvent([{ code: 0 }], false);
started = 0; SP.play(posMap);
ok(started === 0 && SP.playing === false, '事件页无指令（length<=1）-> 不触发');
// 回归：没有任何事件页条件满足时 _pageIndex = -1，page() 是 undefined。
// MV 的 list() 就是 this.page().list，会抛 "Cannot read property 'list' of undefined"
const evNoPage = mkEvent(null, false);
ok(SP.pageListOf(evNoPage) === null, 'pageListOf 对无生效页返回 null');
started = 0; reset(); mapId = mapItem[0];
fakeEvents[mapItem[1]] = evNoPage;
let threw = null;
try { SP.play(posMap); } catch (e) { threw = e; }
ok(threw === null, '无生效页时不抛异常' + (threw ? ' -> ' + threw.message : ''));
ok(started === 0 && SP.playing === false, '无生效页 -> 不触发、不进入播放态');
const evPageThrows = { isStarting: () => false, start: () => { started++; },
                       page: () => { throw new Error('boom'); } };
ok(SP.pageListOf(evPageThrows) === null, 'page() 抛错时 pageListOf 也返回 null');
// 非标准实现（只有 list()，没有 page()）：回退到 list() 且不抛
const evListOnly = { isStarting: () => false, start: () => { started++; },
                     list: () => [{ code: 0 }, { code: 1 }] };
ok(SP.pageListOf(evListOnly).length === 2, '只有 list() 的实现能回退取到指令表');
const evListThrows = { isStarting: () => false, start: () => { started++; },
                       list: () => { throw new Error('boom'); } };
ok(SP.pageListOf(evListThrows) === null, 'list() 抛错时也返回 null');
fakeEvents[mapItem[1]] = mkEvent([{ code: 0 }, { code: 1 }], true);
started = 0; SP.play(posMap);
ok(started === 0 && SP.playing === true, '事件已在 starting 状态 -> 不重复 start，但仍进入播放态');
fakeEvents[mapItem[1]] = mkEvent([{ code: 0 }, { code: 1 }], false);
started = 0; evRunning = true;
SP.play(posMap);
ok(started === 0, '已有事件在运行时不会重复触发');
evRunning = false;

console.log('== 连播在筛选范围内 + 跳过缺素材 ==');
reset();
SP.setFilter('h');
SP.auto = true; SP.playing = true; SP.grace = 0; SP.wait = 0;
SP.last = 0;
reserved = [];
SP.update();
ok(reserved.length === 1, '自动连播触发了一个场景');
const landed = SP.view[SP.last];
ok(landed && landed.tag === 'h', '落点仍在「仅H」范围内: ' + landed.name);
ok(!P_MISS[landed.key], '落点不是缺素材场景');
SP.auto = false; SP.playing = false;
SP.setFilter('all');
const missPosAll = SP.view.findIndex(i => P_MISS[i.key]);
SP.last = missPosAll - 1;
reset();
SP.playNext();
ok(reserved.length === 1 && !P_MISS[String(reserved[0])], 'playNext 跳过缺素材，落到 #' + reserved[0]);

console.log('== 自动推进对话（F10）==');
// 迷你 Window_Message：按 rpg_windows.js 的真实分支顺序建模，专门用来复现
// 「只清 pause 不 terminateMessage -> $gameMessage 仍 busy -> canStart() 又
// startMessage() -> 一直重复当前对话」这个 bug。
function mkMessageWindow(opts) {
    opts = opts || {};
    return {
        pause: opts.pause !== undefined ? opts.pause : true,
        _textState: opts.textState !== undefined ? opts.textState : null,  // null = 文本已播完
        _waitCount: 0,
        terminated: false,
        restarted: false,          // 是否发生了「重复显示同一段对话」
        isAnySubWindowActive: () => !!opts.subWindow,
        terminateMessage: function () {
            this.terminated = true;
            global.$gameMessage.clear();      // MV: close() + $gameMessage.clear()
        },
        // 复刻 Window_Message.update() 里与本 bug 相关的分支顺序
        update: function () {
            if (this._waitCount > 0) { this._waitCount--; return; }   // updateWait
            if (this.pause) { return; }                               // updateInput -> 等待按键
            if (this._textState) { return; }                          // updateMessage 继续处理
            if (global.$gameMessage.isBusy()) { this.restarted = true; }  // canStart -> startMessage
        }
    };
}

msgBusy = true;
SP.msgAuto = false; SP.msgDelay = 3;
const attach = m => { SceneManager._scene = Object.assign(new Scene_Map(), { _messageWindow: m }); };
let mw = mkMessageWindow({});
attach(mw);
SP.updateMessageAuto();
ok(mw.pause === true, '未开 F10 时不动对话');

SP.msgAuto = true;
SP.msgWait = 0;
SP.updateMessageAuto();
ok(mw.pause === false, 'F10 开启后自动翻页（pause 被清）');
ok(mw.terminated === true, '同时调用了 terminateMessage（清掉 $gameMessage）');
ok(msgBusy === false, '$gameMessage 不再 busy');
mw.update();
ok(mw.restarted === false, '不会重新 startMessage -> 不重复当前对话');

// 回归对照：如果只清 pause 不 terminateMessage（v2.0.0 的行为），就会重复
msgBusy = true;
const buggy = mkMessageWindow({});
buggy.pause = false;                 // 模拟「只清 pause」
buggy.update();
ok(buggy.restarted === true, '对照：只清 pause 时确实会重复同一段对话（说明本测试有效）');
msgBusy = true;

// 中途 pause（例如 \| 等待码），_textState 非 null：只清 pause，不该 terminate
mw = mkMessageWindow({ textState: { index: 3, text: 'abc' } });
attach(mw);
SP.msgWait = 0;
SP.updateMessageAuto();
ok(mw.pause === false && mw.terminated === false, '_textState 非 null 时只清 pause，不 terminate');

// 有选项/数字输入时不自动选
mw = mkMessageWindow({ subWindow: true });
attach(mw);
SP.msgWait = 0;
SP.updateMessageAuto();
ok(mw.pause === true && mw.terminated === false, '有选项窗口时不自动翻页');

// 间隔未到不动
mw = mkMessageWindow({});
attach(mw);
SP.msgWait = 99;
SP.updateMessageAuto();
ok(mw.pause === true, 'msgDelay 未到时不翻页');

// 不在 Scene_Map 上时不动作
SP.msgWait = 0;
SceneManager._scene = { _messageWindow: mw };
SP.updateMessageAuto();
ok(mw.pause === true, '不在场景地图上时不动作');

// 对话不 busy 时不动作
msgBusy = false;
attach(mw);
SP.msgWait = 0;
SP.updateMessageAuto();
ok(mw.pause === true, '没有对话在显示时不动作');
SP.msgAuto = false;
msgBusy = false;

console.log('== 影片/图片索引（真实文件系统）==');
const tmp = '/tmp/sp_fs';
fs.rmSync(tmp, { recursive: true, force: true });
fs.mkdirSync(tmp + '/www/img/pictures', { recursive: true });
fs.mkdirSync(tmp + '/www/movies', { recursive: true });
fs.writeFileSync(tmp + '/www/img/pictures/BlackImage.rpgmvp', '');
fs.writeFileSync(tmp + '/www/movies/SomeMovie.webm', '');
const cwd0 = process.cwd();
process.chdir(tmp);
global.Utils = { isNwjs: () => true };
SP._picTried = false; SP._picSet = null; SP._movieSet = null;
SP.initAssetIndex();
ok(SP._picBase === 'www/img/pictures/', '图片目录定位: ' + SP._picBase);
ok(SP._movieBase === 'www/movies/', '影片目录定位: ' + SP._movieBase);
ok(SP.assetMissing('BlackImage') === false, '存在的图片 -> 不缺失');
ok(SP.assetMissing('SomeMovie') === true, '不带 movie: 前缀的名字按图片查，影片名会判缺失（前缀是必须的）');
ok(SP.assetMissing('movie:SomeMovie') === false, '存在的影片 -> 不缺失');
ok(SP.assetMissing('movie:NoSuchMovie') === true, '不存在的影片 -> 缺失');
for (const n of P_MISS['295']) {
    if (n.startsWith('movie:')) fs.writeFileSync(tmp + '/www/movies/' + n.slice(6) + '.webm', '');
    else fs.writeFileSync(tmp + '/www/img/pictures/' + n + '.rpgmvp', '');
}
// 索引是启动时建立并缓存的（真实使用中补素材后重启游戏即可），这里手动重建
SP._picTried = false; SP._picSet = null; SP._movieSet = null;
SP.initAssetIndex();
ok(SP.missingOf(i295).length === 0, '补齐资产并重建索引后 #295 不再缺（实际 ' + SP.missingOf(i295).length + '）');
ok(SP.canPlay(i295) === true, '补齐后可播');
process.chdir(cwd0);

console.log('== 列表绘制 ==');
// 上一步的 fs 测试把 #295 的素材补齐了，这里退回离线模式，验证「缺素材」的显示
global.Utils = { isNwjs: () => false };
SP._picTried = false; SP._picSet = null; SP._movieSet = null;
const w = _oc(Window_SceneListProto);
w.initialize(0, 0, 1008, 648);
SP.setFilter('all');
w._data = SP.view;
w.drawItem(i295);
ok(/\[(H|剧情|杂项)\]/.test(w._drawn[0].t), '第1行带类型标签: ' + JSON.stringify(w._drawn[0].t.trim()));
ok(w._drawn[0].t.includes('⚠缺素材'), '缺素材标 ⚠');
ok(w._drawn[1].t.includes('项（图/影片）'), '第2行说明缺的是图/影片: ' + JSON.stringify(w._drawn[1].t.slice(0, 30)));
w._drawn = []; w.drawItem(posMap);
ok(w._drawn[0].t.includes('🗺'), '地图场景带 🗺 标记: ' + JSON.stringify(w._drawn[0].t.trim()));
ok(w._drawn[1].t.includes('Map'), '地图场景第二行显示 Map 坐标: ' + JSON.stringify(w._drawn[1].t.slice(0, 24)));
w._drawn = []; w.drawItem(posCE);
ok(!w._drawn[0].t.includes('⚠'), '正常场景无 ⚠');
// 子场景（需先显示出来才有位置）
SP.showSub = true; SP.applyFilter();
const posSub = SP.view.findIndex(i => i.subOf);
w._data = SP.view;
w._drawn = []; w.drawItem(posSub);
ok(w._drawn[0].t.includes('⊂子场景'), '子场景标 ⊂子场景: ' + JSON.stringify(w._drawn[0].t.trim().slice(-20)));
ok(w._drawn[1].t.includes('⊂ 被「'), '第二行显示被谁调用: ' + JSON.stringify(w._drawn[1].t.slice(0, 34)));
SP.showSub = true; SP.applyFilter(); w._data = SP.view;
ok(w.itemHeight() === 72, 'itemHeight = 72（两行）');

console.log('== 列表画面与帮助文本 ==');
SceneManager._scene = _oc(Scene_ScenePlayerProto);
SceneManager._scene.create();
ok(!!SceneManager._scene._listWindow && !!SceneManager._scene._helpWindow, '列表窗 + 帮助窗已创建');
ok(SceneManager._scene._helpWindow._text.includes('F6 筛选'), '帮助文本含 F6 筛选提示');
SP.setFilter('h');
ok(SceneManager._scene._helpWindow._text.includes('仅H'), '切筛选后帮助文本同步');

console.log('== 场景钩子 ==');
const sm = _oc(Scene_Map.prototype);
sm.createAllWindows();
ok(!!sm._spToast, '提示窗已挂载');
sm.update();
ok(sm.updated === 1, '原 Scene_Map.update 仍被调用');
ok(Input.keyMapper[36] === 'spHome' && Input.keyMapper[35] === 'spEnd', 'Home/End 已映射');

console.log('\n结果: ' + pass + ' 通过 / ' + fail + ' 失败');
process.exit(fail ? 1 : 0);
