//=============================================================================
// ScenePlayer.js
//=============================================================================
/*:
 * @plugindesc v1.0 场景速播器：场景列表(F7) / 单键下一个(F8) / 自动连播(F9) / 自动推进对话(F10)
 * @author custom
 *
 * @param sceneList
 * @text 场景列表(JSON)
 * @desc [[id,"名称"],...] 形式。留空则不做任何事。
 * @type string
 * @default []
 *
 * @param openKey
 * @text 打开列表按键(keyCode)
 * @desc 默认 118 = F7
 * @type number
 * @default 118
 *
 * @param nextKey
 * @text 播放下一个按键(keyCode)
 * @desc 默认 119 = F8
 * @type number
 * @default 119
 *
 * @param autoKey
 * @text 自动连播开关(keyCode)
 * @desc 默认 120 = F9
 * @type number
 * @default 120
 *
 * @param msgKey
 * @text 自动推进对话开关(keyCode)
 * @desc 默认 121 = F10
 * @type number
 * @default 121
 *
 * @param autoDelay
 * @text 自动连播间隔(帧)
 * @desc 一个场景结束后等多少帧播下一个，60帧≈1秒
 * @type number
 * @default 60
 *
 * @param msgDelay
 * @text 自动推进对话间隔(帧)
 * @desc 对话完全显示后等多少帧自动翻页，45帧≈0.75秒
 * @type number
 * @default 45
 *
 * @param filterKey
 * @text 切换类型筛选按键(keyCode)
 * @desc 默认 117 = F6，循环切换 全部 / 仅H / 仅剧情 / 仅杂项
 * @type number
 * @default 117
 *
 * @param mapScenes
 * @text 地图事件场景(JSON)
 * @desc [[mapId, eventId, x, y, 显示名, 原始名], ...]。播放时会先传送到该地图再触发事件。
 * @type string
 * @default []
 *
 * @param tags
 * @text 场景类型标签(JSON)
 * @desc {"键":"h|story|misc"}，键为公共事件 id 或 "m<mapId>:<eventId>"。用于筛选与列表显示。
 * @type string
 * @default {}
 *
 * @param missingAssets
 * @text 缺素材清单(JSON)
 * @desc {"场景id":["图片名",...]}。列表里标⚠、自动连播跳过。NW.js 下会实时读
 *       img/pictures 复核：若素材已装上则自动放行。
 * @type string
 * @default {}
 *
 * @help
 * ============================================================================
 * 用途：不用再在作弊菜单里一个个点，直接用快捷键连着看公共事件（场景）。
 * ============================================================================
 *
 * 【快捷键】（只在场景地图上生效）
 *   F7  打开场景列表窗口
 *   F8  直接播放下一个场景（按住可连续推进）
 *   F9  自动连播开关：当前场景一结束，自动播下一个
 *   F10 自动推进对话开关：对话显示完整后自动翻页（有选项时不会自动选）
 *
 * 【列表窗口内】
 *   ↑ / ↓     上下选择
 *   ← / →     一次跳 10 个
 *   PgUp/PgDn 翻页
 *   Home/End  跳到首/尾
 *   Enter     播放选中场景并关闭窗口
 *   Esc       关闭窗口
 *
 * 【控制台脚本调用】（F8 之外的备用方式）
 *   ScenePlayer.playNext()      播放下一个
 *   ScenePlayer.play(i)         播放列表第 i 个（0 起）
 *   ScenePlayer.playId(1257)    按公共事件 id 播放
 *   ScenePlayer.toggleAuto()    切换自动连播
 *   ScenePlayer.scenes          当前场景列表
 *   ScenePlayer.status()        打印当前状态
 *
 * 【注意】
 *   本插件只做「触发公共事件」，不修改存档数据。但被触发的场景本身可能会
 *   改变开关/变量/物品，建议先用独立存档测试。
 * ============================================================================
 */

(function() {
    'use strict';

    if (typeof Scene_Map === 'undefined' || typeof Window_Selectable === 'undefined') {
        console.error('ScenePlayer: 不是 RPG Maker MV 环境，插件已跳过');
        return;
    }

    var PLUGIN = 'ScenePlayer';
    var params = PluginManager.parameters(PLUGIN);

    function toInt(v, d) {
        var n = parseInt(v, 10);
        return isNaN(n) ? d : n;
    }

    function parseScenes(raw) {
        var data;
        try {
            data = JSON.parse(raw || '[]');
        } catch (e) {
            console.error(PLUGIN + ': sceneList 不是合法 JSON', e);
            return [];
        }
        if (!(data instanceof Array)) { return []; }
        var out = [];
        for (var i = 0; i < data.length; i++) {
            var it = data[i];
            var id, name, orig = '';
            if (typeof it === 'number') {
                id = it;
                name = '#' + it;
            } else if (it instanceof Array) {
                id = it[0];
                name = it[1];
                orig = it[2] || '';
            } else if (it && typeof it === 'object') {
                id = it.id;
                name = it.name;
                orig = it.orig || '';
            } else {
                continue;
            }
            id = Number(id);
            if (id === undefined || id === null || isNaN(id)) { continue; }
            if (name === undefined || name === null || name === '') { name = '#' + id; }
            out.push({ id: id, name: String(name), orig: String(orig) });
        }
        return out;
    }

    var SCENES = parseScenes(params['sceneList']);
    var MAP_SCENES = parseMapScenes(params['mapScenes']);
    var MISSING = parseMissing(params['missingAssets']);
    var TAGS = parseTags(params['tags']);
    var KEY_OPEN = toInt(params['openKey'], 118);
    var KEY_NEXT = toInt(params['nextKey'], 119);
    var KEY_AUTO = toInt(params['autoKey'], 120);
    var KEY_MSG = toInt(params['msgKey'], 121);
    var KEY_FILTER = toInt(params['filterKey'], 117);   // F6
    var AUTO_DELAY = toInt(params['autoDelay'], 60);
    var MSG_DELAY = toInt(params['msgDelay'], 45);

    // 地图场景：[[mapId, eventId, x, y, 显示名, 原始名], ...]
    function parseMapScenes(raw) {
        var data, out = [];
        try {
            data = JSON.parse(raw || '[]');
        } catch (e) {
            console.error(PLUGIN + ': mapScenes 不是合法 JSON', e);
            return out;
        }
        if (!(data instanceof Array)) { return out; }
        for (var i = 0; i < data.length; i++) {
            var it = data[i];
            if (!(it instanceof Array) || it.length < 2) { continue; }
            var mapId = Number(it[0]), eventId = Number(it[1]);
            if (isNaN(mapId) || isNaN(eventId)) { continue; }
            out.push({
                kind: 'map',
                mapId: mapId,
                eventId: eventId,
                x: Number(it[2]) || 0,
                y: Number(it[3]) || 0,
                name: String(it[4] || ('地图事件 ' + mapId + ':' + eventId)),
                orig: String(it[5] || ('Map' + mapId + ' #' + eventId)),
                key: 'm' + mapId + ':' + eventId
            });
        }
        return out;
    }

    // 类型标签：{"295":"h", "m8:3":"h", ...}
    function parseTags(raw) {
        var obj, out = {};
        try {
            obj = JSON.parse(raw || '{}');
        } catch (e) {
            console.error(PLUGIN + ': tags 不是合法 JSON', e);
            return out;
        }
        if (!obj || typeof obj !== 'object') { return out; }
        for (var k in obj) {
            if (obj.hasOwnProperty(k) && (obj[k] === 'h' || obj[k] === 'story' || obj[k] === 'misc')) {
                out[k] = obj[k];
            }
        }
        return out;
    }

    var TAG_LABEL = { h: 'H', story: '剧情', misc: '杂项' };
    var FILTERS = ['all', 'h', 'story', 'misc'];
    var FILTER_LABEL = { all: '全部', h: '仅H', story: '仅剧情', misc: '仅杂项' };

    // 缺素材清单：{"295":["DaughterBedScene - 001", ...], ...}
    function parseMissing(raw) {
        var obj, out = {};
        try {
            obj = JSON.parse(raw || '{}');
        } catch (e) {
            console.error(PLUGIN + ': missingAssets 不是合法 JSON', e);
            return out;
        }
        if (!obj || typeof obj !== 'object') { return out; }
        for (var k in obj) {
            if (!obj.hasOwnProperty(k)) { continue; }
            if (!(obj[k] instanceof Array)) { continue; }
            // 键既可能是公共事件 id（"295"），也可能是地图场景（"m8:3"）
            if (k.indexOf('m') === 0) {
                out[k] = obj[k].map(String);
            } else {
                var id = Number(k);
                if (isNaN(id)) { continue; }
                out[id] = obj[k].map(String);
            }
        }
        return out;
    }


    //-------------------------------------------------------------------------
    // ScenePlayer (全局对象)
    //-------------------------------------------------------------------------

    var SP = {};
    window.ScenePlayer = SP;

    SP.scenes = SCENES;    // 公共事件场景（保持向后兼容）
    SP.mapScenes = MAP_SCENES;
    SP.tags = TAGS;
    SP.items = buildItems();
    SP.filter = 'all';
    SP.view = [];
    SP.index = 0;          // 列表光标位置（相对 SP.view）
    SP.last = -1;          // 上次播放的位置（相对 SP.view）
    SP.lastKey = null;     // 上次播放场景的键，切换筛选时用来定位
    SP.pending = null;     // 等待传送完成后再触发的场景
    SP.pendingWait = 0;
    SP.auto = false;       // 自动连播
    SP.msgAuto = false;    // 自动推进对话
    SP.playing = false;    // 已触发、等待结束
    SP.grace = 0;          // 触发后宽限帧（等解释器真正跑起来）
    SP.wait = 0;           // 结束后的倒计时
    SP.msgWait = 0;        // 对话自动推进倒计时
    SP.msgDelay = MSG_DELAY;
    SP._picSet = null;     // img/pictures 文件名索引（延迟建立）
    SP._picBase = null;    // 实际生效的目录前缀
    SP._movieSet = null;   // movies 文件名索引
    SP._movieBase = null;
    SP._picTried = false;  // 是否已经尝试过建立索引

    // 合并公共事件场景与地图场景（公共事件在前，地图场景在后）
    function buildItems() {
        var out = [], i;
        for (i = 0; i < SCENES.length; i++) {
            out.push({
                kind: 'ce',
                id: SCENES[i].id,
                name: SCENES[i].name,
                orig: SCENES[i].orig,
                key: String(SCENES[i].id),
                tag: TAGS[String(SCENES[i].id)] || 'h'
            });
        }
        for (i = 0; i < MAP_SCENES.length; i++) {
            var m = MAP_SCENES[i];
            m.tag = TAGS[m.key] || 'story';
            out.push(m);
        }
        return out;
    }

    // 按当前筛选重建可见列表
    SP.applyFilter = function() {
        var out = [];
        for (var i = 0; i < SP.items.length; i++) {
            if (SP.filter === 'all' || SP.items[i].tag === SP.filter) {
                out.push(SP.items[i]);
            }
        }
        SP.view = out;
        // 尽量把光标和「上次播放」定位回原场景
        SP.index = 0;
        SP.last = -1;
        for (var k = 0; k < out.length; k++) {
            if (out[k].key === SP.lastKey) { SP.last = k; SP.index = k; }
        }
        return out;
    };

    SP.setFilter = function(f) {
        if (FILTERS.indexOf(f) < 0) { return; }
        SP.filter = f;
        SP.applyFilter();
        SP.refreshHelp();
        SP.refreshList();
    };

    SP.cycleFilter = function() {
        var i = FILTERS.indexOf(SP.filter);
        var next = FILTERS[(i + 1) % FILTERS.length];
        SP.setFilter(next);
        SP.toast('筛选：' + FILTER_LABEL[next] + '（' + SP.view.length + ' 个场景）');
    };

    SP.itemOf = function(i) {
        return SP.view[i];
    };

    SP.countByTag = function(tag) {
        var n = 0;
        for (var i = 0; i < SP.items.length; i++) {
            if (SP.items[i].tag === tag) { n++; }
        }
        return n;
    };

    //-------------------------------------------------------------------------
    // 素材存在性检查（NW.js 下真去读目录；否则退回离线标记）
    //-------------------------------------------------------------------------

    SP.initAssetIndex = function() {
        if (SP._picTried) { return; }
        SP._picTried = true;
        try {
            if (typeof Utils === 'undefined' || !Utils.isNwjs() || typeof require !== 'function') { return; }
            var fs = require('fs');
            var i, k;

            // 图片：img/pictures。用一张必然存在的通用图自检目录是否选对。
            var bases = ['www/img/pictures/', 'img/pictures/'];
            for (i = 0; i < bases.length; i++) {
                if (!fs.existsSync(bases[i])) { continue; }
                var files = fs.readdirSync(bases[i]);
                var set = {};
                for (k = 0; k < files.length; k++) {
                    set[files[k].replace(/\.(rpgmvp|png|jpg|jpeg|webp)$/i, '')] = true;
                }
                if (set['BlackImage']) {
                    SP._picBase = bases[i];
                    SP._picSet = set;
                    break;
                }
            }

            // 影片：movies。缺失的影片会让 MV 反复重试加载（每个约 4.5 秒）把游戏卡住，
            // 所以必须一起检测。
            var mbases = ['www/movies/', 'movies/'];
            for (i = 0; i < mbases.length; i++) {
                if (!fs.existsSync(mbases[i])) { continue; }
                var mfiles = fs.readdirSync(mbases[i]);
                if (!mfiles.length) { continue; }
                var mset = {};
                for (k = 0; k < mfiles.length; k++) {
                    mset[mfiles[k].replace(/\.(webm|mp4|m4v|ogg)$/i, '')] = true;
                }
                SP._movieBase = mbases[i];
                SP._movieSet = mset;
                break;
            }

            console.log('[ScenePlayer] 素材索引：图片 ' + (SP._picSet ? SP._picBase : '不可用')
                + '，影片 ' + (SP._movieSet ? SP._movieBase : '不可用'));
            if (!SP._picSet) { console.warn('[ScenePlayer] 未能定位 img/pictures，图片检测退回离线标记'); }
            if (!SP._movieSet) { console.warn('[ScenePlayer] 未能定位 movies，影片检测退回离线标记'); }
        } catch (e) {
            console.warn('[ScenePlayer] 素材索引失败，退回离线标记:', e);
        }
    };

    // 单个资产是否缺失；'movie:xxx' 表示影片，其余为图片
    SP.assetMissing = function(name) {
        var isMovie = name.indexOf('movie:') === 0;
        var set = isMovie ? SP._movieSet : SP._picSet;
        if (!set) { return true; }               // 该类索引没建起来 → 保守按缺失处理
        return !set[isMovie ? name.slice(6) : name];
    };

    // 返回该场景当前真正缺失的资产（空数组 = 可播）
    SP.missingOf = function(i) {
        var s = SP.view[i];
        if (!s) { return []; }
        var list = MISSING[s.key];
        if (!list || !list.length) { return []; }
        SP.initAssetIndex();
        if (!SP._picSet && !SP._movieSet) { return list; }   // 完全探测不了 → 按离线标记
        var out = [];
        for (var k = 0; k < list.length; k++) {
            if (SP.assetMissing(list[k])) { out.push(list[k]); }
        }
        return out;
    };

    SP.canPlay = function(i) {
        return SP.missingOf(i).length === 0;
    };

    SP.checkAssets = function() {
        var bad = [];
        for (var i = 0; i < SP.items.length; i++) {
            var list = MISSING[SP.items[i].key];
            if (!list || !list.length) { continue; }
            SP.initAssetIndex();
            SP.initAssetIndex();
            var gone = list.filter(function (n) { return SP.assetMissing(n); });
            if (gone.length) {
                bad.push(SP.items[i].key + ' ' + SP.items[i].name + ' (缺' + gone.length + ')');
            }
        }
        var txt = bad.length
            ? ('缺素材场景 ' + bad.length + '/' + SP.items.length + '：\n' + bad.join('\n'))
            : ('全部 ' + SP.items.length + ' 个场景素材齐全');
        console.log(txt);
        return txt;
    };

    SP.busy = function() {
        if (typeof SceneManager.isSceneChanging === 'function' && SceneManager.isSceneChanging()) { return true; }
        if ($gameMessage.isBusy()) { return true; }
        if ($gamePlayer.isTransferring()) { return true; }
        if ($gameMap.isEventRunning()) { return true; }
        return false;
    };

    SP.play = function(i) {
        if (!SP.view.length) { SP.toast('当前筛选下没有场景'); return false; }
        i = Number(i);
        if (isNaN(i) || i < 0 || i >= SP.view.length) { return false; }
        var it = SP.view[i];
        if (!SP.canPlay(i)) {
            SP.toast('⚠ 跳过「' + it.name + '」：缺素材（图/影片）');
            return false;
        }
        if (SP.busy()) { SP.toast('当前有事件/对话在运行，稍后再按'); return false; }
        SP.index = i;
        SP.last = i;
        SP.lastKey = it.key;
        if (it.kind === 'map') {
            return SP.playMapScene(it);
        }
        $gameTemp.reserveCommonEvent(it.id);
        SP.playing = true;
        SP.grace = 20;
        SP.wait = AUTO_DELAY;
        SP.toast('▶ ' + (i + 1) + '/' + SP.view.length + '  ' + it.name + '  (#' + it.id + ')'
            + (SP.auto ? '   [自动连播]' : ''));
        return true;
    };

    // 地图场景：先传送到目标地图，再让事件自己跑起来
    SP.playMapScene = function(it) {
        if ($gameMap.mapId() !== it.mapId) {
            $gamePlayer.reserveTransfer(it.mapId, it.x, it.y, 2, 0);
            SP.pending = it;
            SP.pendingWait = 600;          // 最多等 10 秒
            SP.playing = true;
            SP.grace = 30;
            SP.wait = AUTO_DELAY;
            SP.toast('🗺 前往「' + it.name + '」(Map' + it.mapId + ') …');
            return true;
        }
        return SP.startMapEvent(it, false);
    };

    // 真正触发地图事件：只设 _starting 标志，MV 的 Game_Map.setupStartingMapEvent 会
    // 在 updateInterpreter 里 setup 解释器、并在结束后 unlock，和玩家自己触发完全一致。
    SP.startMapEvent = function(it, alreadyRunning) {
        var ev = $gameMap.event(it.eventId);
        if (!ev) {
            SP.toast('⚠ Map' + it.mapId + ' 上找不到事件 #' + it.eventId);
            return false;
        }
        // 玩家接触型的事件可能在传送落地时就自己触发了，别重复开
        var running = alreadyRunning || ev.isStarting() || $gameMap.isEventRunning();
        if (!running) {
            var list = ev.list();
            if (!list || list.length <= 1) {
                SP.toast('⚠「' + it.name + '」当前事件页没有指令（页条件未满足）');
                return false;
            }
            ev.start();
        }
        SP.playing = true;
        SP.grace = running ? 5 : 20;
        SP.wait = AUTO_DELAY;
        SP.toast('▶ ' + it.name + '  (Map' + it.mapId + ' #' + it.eventId + ')'
            + (SP.auto ? '   [自动连播]' : ''));
        return true;
    };

    SP.playId = function(id) {
        var target = null, i;
        for (i = 0; i < SP.items.length; i++) {
            if (SP.items[i].kind === 'ce' && SP.items[i].id === Number(id)) { target = SP.items[i]; break; }
        }
        if (target) {
            var pos = SP.view.indexOf(target);
            if (pos >= 0) { return SP.play(pos); }
        }
        // 不在当前筛选范围也允许直接播（仅公共事件）
        if (SP.busy()) { SP.toast('当前有事件/对话在运行，稍后再按'); return false; }
        $gameTemp.reserveCommonEvent(Number(id));
        SP.playing = true;
        SP.grace = 20;
        SP.toast('▶ 直接播放 #' + id);
        return true;
    };

    SP.playMap = function(mapId, eventId) {
        var key = 'm' + Number(mapId) + ':' + Number(eventId);
        for (var i = 0; i < SP.items.length; i++) {
            if (SP.items[i].key === key) {
                var pos = SP.view.indexOf(SP.items[i]);
                if (pos >= 0) { return SP.play(pos); }
                SP.toast('该场景不在当前筛选范围（' + FILTER_LABEL[SP.filter] + '），先按 F6 切换');
                return false;
            }
        }
        SP.toast('列表里没有地图场景 ' + key);
        return false;
    };

    // 从 from 之后找第一个能播的（跳过缺素材的）
    SP.findPlayable = function(from) {
        var n = SP.view.length;
        for (var k = 1; k <= n; k++) {
            var i = ((from + k) % n + n) % n;
            if (SP.canPlay(i)) { return i; }
        }
        return -1;
    };

    SP.playNext = function() {
        if (!SP.view.length) { SP.toast('当前筛选下没有场景'); return false; }
        var i = SP.findPlayable(SP.last);
        if (i < 0) { SP.toast('没有可播放的场景（全部缺素材）'); return false; }
        return SP.play(i);
    };

    SP.playPrev = function() {
        var n = SP.view.length;
        if (!n) { return false; }
        for (var k = 1; k <= n; k++) {
            var i = ((SP.last - k) % n + n) % n;
            if (SP.canPlay(i)) { return SP.play(i); }
        }
        return false;
    };

    SP.toggleAuto = function() {
        SP.auto = !SP.auto;
        if (SP.auto) {
            SP.wait = AUTO_DELAY;
            SP.toast('自动连播：开  (F9 关闭)');
            if (!SP.playing) { SP.playNext(); }
        } else {
            SP.toast('自动连播：关');
        }
        SP.refreshHelp();
    };

    SP.toggleMsgAuto = function() {
        SP.msgAuto = !SP.msgAuto;
        SP.msgWait = 0;
        SP.toast('自动推进对话：' + (SP.msgAuto ? '开' : '关') + '  (F10 切换)');
        SP.refreshHelp();
    };

    SP.status = function() {
        var s = (SP.last >= 0 && SP.view[SP.last]) ? SP.view[SP.last].name : '(未播放)';
        var txt = 'ScenePlayer: 共' + SP.items.length + '个（公共事件' + SCENES.length
            + ' + 地图' + MAP_SCENES.length + '）| 筛选=' + FILTER_LABEL[SP.filter]
            + '(' + SP.view.length + ') | 上次=' + s
            + ' | 连播=' + (SP.auto ? '开' : '关') + ' | 自动对话=' + (SP.msgAuto ? '开' : '关');
        console.log(txt);
        return txt;
    };

    SP.toast = function(text) {
        var scene = SceneManager._scene;
        if (scene && scene._spToast) { scene._spToast.show(text); }
        console.log('[ScenePlayer] ' + text);
    };

    SP.refreshList = function() {
        var scene = SceneManager._scene;
        if (scene && scene._listWindow && typeof scene._listWindow.setData === 'function') {
            scene._listWindow.setData(SP.view, SP.index);
        }
    };

    SP.refreshHelp = function() {
        var scene = SceneManager._scene;
        if (scene && scene._helpWindow && scene.helpText) {
            scene._helpWindow.setText(scene.helpText());
        }
    };

    SP.update = function() {
        SP.updatePending();
        SP.updateAuto();
        SP.updateMessageAuto();
    };

    // 等待「传送 → 落地 → 触发地图事件」
    SP.updatePending = function() {
        if (!SP.pending) { return; }
        if (SP.pendingWait-- <= 0) {
            SP.pending = null;
            SP.playing = false;
            SP.toast('⚠ 传送超时，已放弃该场景');
            return;
        }
        if ($gamePlayer.isTransferring()) { return; }
        if (typeof SceneManager.isSceneChanging === 'function' && SceneManager.isSceneChanging()) { return; }
        if ($gameMap.mapId() !== SP.pending.mapId) { return; }
        var it = SP.pending;
        SP.pending = null;
        SP.startMapEvent(it, false);
    };

    SP.updateAuto = function() {
        if (SP.pending) { return; }          // 还在传送途中
        if (SP.grace > 0) { SP.grace--; return; }
        if (!SP.playing) { return; }
        if (SP.busy()) { SP.wait = AUTO_DELAY; return; }
        if (SP.wait > 0) { SP.wait--; return; }
        SP.playing = false;
        if (SP.auto && !SP.playNext()) {
            SP.auto = false;          // 无可播场景就停下，避免每帧重试刷屏
            SP.toast('自动连播已停止（没有可播放的场景）');
            SP.refreshHelp();
        }
    };

    SP.updateMessageAuto = function() {
        if (!SP.msgAuto) { SP.msgWait = 0; return; }
        var scene = SceneManager._scene;
        if (!(scene instanceof Scene_Map)) { return; }
        var mw = scene._messageWindow;
        if (!mw || !$gameMessage.isBusy()) { SP.msgWait = 0; return; }
        if (typeof mw.isAnySubWindowActive === 'function' && mw.isAnySubWindowActive()) {
            SP.msgWait = 0;   // 有选项/数字输入时绝不自动选
            return;
        }
        if (mw.pause) {
            if (SP.msgWait > 0) {
                SP.msgWait--;
            } else {
                mw.pause = false;
                SP.msgWait = SP.msgDelay;
            }
        }
    };

    //-------------------------------------------------------------------------
    // 顶部提示窗
    //-------------------------------------------------------------------------

    function Window_SpToast() {
        this.initialize.apply(this, arguments);
    }

    Window_SpToast.prototype = Object.create(Window_Base.prototype);
    Window_SpToast.prototype.constructor = Window_SpToast;

    Window_SpToast.prototype.initialize = function() {
        var w = Math.min(Graphics.boxWidth - 40, 1000);
        var h = this.fittingHeight(1);
        Window_Base.prototype.initialize.call(this, 20, 10, w, h);
        this.opacity = 200;
        this.backOpacity = 200;
        this.visible = false;
        this._frames = 0;
        this.z = 300;
    };

    Window_SpToast.prototype.show = function(text) {
        this.contents.clear();
        this.changeTextColor(this.systemColor());
        this.drawText(text, 0, 0, this.contents.width, 'left');
        this.visible = true;
        this._frames = 240;
    };

    Window_SpToast.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (this._frames > 0 && --this._frames === 0) { this.visible = false; }
    };

    //-------------------------------------------------------------------------
    // 场景列表窗
    //-------------------------------------------------------------------------

    function Window_SceneList() {
        this.initialize.apply(this, arguments);
    }

    Window_SceneList.prototype = Object.create(Window_Selectable.prototype);
    Window_SceneList.prototype.constructor = Window_SceneList;

    Window_SceneList.prototype.initialize = function(x, y, w, h) {
        // 必须在调用父类之前初始化 _data：
        // Window_Selectable.initialize 末尾会 deactivate() -> reselect() -> select()
        // -> ensureCursorVisible() -> maxTopRow() -> maxRows() -> maxItems()，
        // 那时若 _data 还是 undefined 就会 "Cannot read property 'length' of undefined"。
        // MV 的 Window_Command 同样是先 this._list = [] 再调父类。
        this._data = [];
        Window_Selectable.prototype.initialize.call(this, x, y, w, h);
    };

    Window_SceneList.prototype.setData = function(data, index) {
        this._data = data || [];
        this.refresh();
        this.select(index || 0);
        this.activate();
    };

    Window_SceneList.prototype.maxItems = function() {
        return this._data ? this._data.length : 0;
    };
    Window_SceneList.prototype.itemHeight = function() { return this.lineHeight() * 2; };
    Window_SceneList.prototype.updateHelp = function() {};

    // 第 1 行：[标签] 中文名（选中/上次播放会变色；缺素材标 ⚠ 变灰）
    // 第 2 行：英文原名（地图场景显示 MapXXX #id）；缺素材时改为显示缺了多少张
    Window_SceneList.prototype.drawItem = function(index) {
        var it = this._data[index];
        if (!it) { return; }
        var rect = this.itemRectForText(index);
        var lh = this.lineHeight();
        var base = this.standardFontSize();
        var miss = SP.missingOf(index);
        if (miss.length) {
            this.changeTextColor(this.deathColor());
        } else if (index === SP.last) {
            this.changeTextColor(this.powerUpColor());
        } else if (index === SP.index) {
            this.changeTextColor(this.systemColor());
        } else {
            this.resetTextColor();
        }
        var no = String(index + 1);
        while (no.length < 4) { no = ' ' + no; }
        var tag = '[' + (TAG_LABEL[it.tag] || it.tag) + ']';
        var where = it.kind === 'map' ? '🗺' : ' ';
        this.contents.fontSize = base;
        this.drawText(no + ' ' + tag + where + ' #' + (it.kind === 'map' ? it.key : it.id)
            + '  ' + it.name + (miss.length ? '  ⚠缺素材' : ''), rect.x, rect.y, rect.width);
        var sub = miss.length ? ('缺 ' + miss.length + ' 项（图/影片），需 Spicy Mod：' + miss[0]) : it.orig;
        if (sub) {
            var op = this.contents.paintOpacity;
            this.contents.paintOpacity = 130;
            this.contents.fontSize = Math.max(14, base - 8);
            this.drawText(sub, rect.x + 70, rect.y + lh, rect.width - 70);
            this.contents.paintOpacity = op;
            this.contents.fontSize = base;
        }
        this.resetTextColor();
    };

    Window_SceneList.prototype.selectJump = function(i) {
        if (!this.maxItems()) { return; }
        if (i < 0) { i = 0; }
        if (i > this.maxItems() - 1) { i = this.maxItems() - 1; }
        if (i !== this.index()) { this.select(i); }
    };

    Window_SceneList.prototype.processCursorMove = function() {
        if (this.isCursorMovable()) {
            if (Input.isRepeated('right')) { this.selectJump(this.index() + 10); }
            if (Input.isRepeated('left')) { this.selectJump(this.index() - 10); }
            if (Input.isTriggered('spHome')) { this.selectJump(0); }
            if (Input.isTriggered('spEnd')) { this.selectJump(this.maxItems() - 1); }
        }
        Window_Selectable.prototype.processCursorMove.call(this);
    };

    //-------------------------------------------------------------------------
    // 场景列表画面
    //-------------------------------------------------------------------------

    function Scene_ScenePlayer() {
        Scene_MenuBase.call(this);
    }

    Scene_ScenePlayer.prototype = Object.create(Scene_MenuBase.prototype);
    Scene_ScenePlayer.prototype.constructor = Scene_ScenePlayer;

    Scene_ScenePlayer.prototype.create = function() {
        Scene_MenuBase.prototype.create.call(this);
        this.createHelpWindow();
        this.createListWindow();
    };

    Scene_ScenePlayer.prototype.helpText = function() {
        var blocked = 0;
        for (var i = 0; i < SP.view.length; i++) {
            if (!SP.canPlay(i)) { blocked++; }
        }
        return 'F6 筛选：' + FILTER_LABEL[SP.filter] + '（' + SP.view.length + '/' + SP.items.length + ' 个）'
            + '   ↑↓ 选择  ←→ 跳10  PgUp/PgDn 翻页  Enter 播放  Esc 关闭'
            + (blocked ? '   ⚠ 缺素材 ' + blocked + ' 个已跳过' : '')
            + '   连播:' + (SP.auto ? '开' : '关') + ' 自动对话:' + (SP.msgAuto ? '开' : '关');
    };

    Scene_ScenePlayer.prototype.createHelpWindow = function() {
        this._helpWindow = new Window_Help(2);
        this._helpWindow.setText(this.helpText());
        this.addWindow(this._helpWindow);
    };

    Scene_ScenePlayer.prototype.createListWindow = function() {
        var wy = this._helpWindow.height;
        var ww = Graphics.boxWidth;
        var wh = Graphics.boxHeight - wy;
        this._listWindow = new Window_SceneList(0, wy, ww, wh);
        this._listWindow.setHandler('ok', this.onListOk.bind(this));
        this._listWindow.setHandler('cancel', this.popScene.bind(this));
        this.addWindow(this._listWindow);
        this._listWindow.setData(SP.view, SP.index);
        this._listWindow.activate();
    };

    Scene_ScenePlayer.prototype.onListOk = function() {
        var i = this._listWindow.index();
        SP.index = i;
        SP.play(i);
        this.popScene();
    };

    //-------------------------------------------------------------------------
    // 挂钩
    //-------------------------------------------------------------------------

    var _Scene_Map_createAllWindows = Scene_Map.prototype.createAllWindows;
    Scene_Map.prototype.createAllWindows = function() {
        _Scene_Map_createAllWindows.call(this);
        this._spToast = new Window_SpToast();
        this.addWindow(this._spToast);
    };

    var _Scene_Map_update = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() {
        _Scene_Map_update.call(this);
        try {
            SP.update();
        } catch (e) {
            console.error('ScenePlayer.update 出错:', e);
        }
    };

    // Home / End 在 MV 里没有默认映射
    Input.keyMapper[36] = 'spHome';
    Input.keyMapper[35] = 'spEnd';

    function onKeyDown(event) {
        if (event.ctrlKey || event.altKey || event.metaKey) { return; }
        var code = event.keyCode;
        if (code !== KEY_OPEN && code !== KEY_NEXT && code !== KEY_AUTO
            && code !== KEY_MSG && code !== KEY_FILTER) { return; }
        var scene = SceneManager._scene;
        var inMap = (scene instanceof Scene_Map);
        var inList = (scene instanceof Scene_ScenePlayer);

        if (code === KEY_FILTER) {
            if (inMap || inList) {
                event.preventDefault();
                SP.cycleFilter();
            }
            return;
        }
        if (code === KEY_OPEN) {
            if (inMap) {
                event.preventDefault();
                if (!SP.scenes.length) { SP.toast('场景列表为空（插件参数 sceneList 没配）'); return; }
                SceneManager.push(Scene_ScenePlayer);
            }
            return;
        }
        if (!inMap && !inList) { return; }
        event.preventDefault();
        if (code === KEY_NEXT) {
            SP.playNext();
        } else if (code === KEY_AUTO) {
            SP.toggleAuto();
        } else if (code === KEY_MSG) {
            SP.toggleMsgAuto();
        }
    }

    if (typeof window.addEventListener === 'function') {
        window.addEventListener('keydown', onKeyDown, false);
    } else {
        console.warn('[ScenePlayer] 环境不支持 window.addEventListener，快捷键不可用');
    }

    SP.applyFilter();
    console.log('[ScenePlayer] v2.0.0 已加载：公共事件 ' + SCENES.length + ' + 地图事件 '
        + MAP_SCENES.length + ' = ' + SP.items.length + ' 个'
        + '（H ' + SP.countByTag('h') + ' / 剧情 ' + SP.countByTag('story')
        + ' / 杂项 ' + SP.countByTag('misc') + '）'
        + '  | F6 筛选  F7 列表  F8 下一个  F9 连播  F10 自动对话');
})();
