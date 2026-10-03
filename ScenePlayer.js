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
    var MISSING = parseMissing(params['missingAssets']);
    var KEY_OPEN = toInt(params['openKey'], 118);
    var KEY_NEXT = toInt(params['nextKey'], 119);
    var KEY_AUTO = toInt(params['autoKey'], 120);
    var KEY_MSG = toInt(params['msgKey'], 121);
    var AUTO_DELAY = toInt(params['autoDelay'], 60);
    var MSG_DELAY = toInt(params['msgDelay'], 45);

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
            var id = Number(k);
            if (isNaN(id) || !(obj[k] instanceof Array)) { continue; }
            out[id] = obj[k].map(String);
        }
        return out;
    }


    //-------------------------------------------------------------------------
    // ScenePlayer (全局对象)
    //-------------------------------------------------------------------------

    var SP = {};
    window.ScenePlayer = SP;

    SP.scenes = SCENES;
    SP.index = 0;          // 列表光标位置
    SP.last = -1;          // 上次播放的下标
    SP.auto = false;       // 自动连播
    SP.msgAuto = false;    // 自动推进对话
    SP.playing = false;    // 已触发、等待结束
    SP.grace = 0;          // 触发后宽限帧（等解释器真正跑起来）
    SP.wait = 0;           // 结束后的倒计时
    SP.msgWait = 0;        // 对话自动推进倒计时
    SP.msgDelay = MSG_DELAY;
    SP._picSet = null;     // img/pictures 文件名索引（延迟建立）
    SP._picBase = null;    // 实际生效的目录前缀
    SP._picTried = false;  // 是否已经尝试过建立索引

    //-------------------------------------------------------------------------
    // 素材存在性检查（NW.js 下真去读目录；否则退回离线标记）
    //-------------------------------------------------------------------------

    SP.initAssetIndex = function() {
        if (SP._picTried) { return; }
        SP._picTried = true;
        try {
            if (typeof Utils === 'undefined' || !Utils.isNwjs() || typeof require !== 'function') { return; }
            var fs = require('fs');
            // package.json 的 main 是 www/index.html，cwd 在游戏根目录；两种都试
            var bases = ['www/img/pictures/', 'img/pictures/'];
            for (var i = 0; i < bases.length; i++) {
                var b = bases[i];
                if (!fs.existsSync(b)) { continue; }
                var files = fs.readdirSync(b);
                var set = {};
                for (var k = 0; k < files.length; k++) {
                    set[files[k].replace(/\.(rpgmvp|png|jpg|jpeg|webp)$/i, '')] = true;
                }
                if (set['BlackImage']) {   // 自检：这张通用图必然存在，能确认目录选对了
                    SP._picBase = b;
                    SP._picSet = set;
                    console.log('[ScenePlayer] 素材索引就绪: ' + b + ' (' + files.length + ' 个文件)');
                    return;
                }
            }
            console.warn('[ScenePlayer] 未能定位 img/pictures，缺素材检测退回离线标记');
        } catch (e) {
            console.warn('[ScenePlayer] 素材索引失败，退回离线标记:', e);
        }
    };

    // 返回该场景当前真正缺失的图片名（空数组 = 可播）
    SP.missingOf = function(i) {
        var s = SCENES[i];
        if (!s) { return []; }
        var list = MISSING[s.id];
        if (!list || !list.length) { return []; }
        SP.initAssetIndex();
        if (!SP._picSet) { return list; }        // 探测不了就按离线标记全缺
        var out = [];
        for (var k = 0; k < list.length; k++) {
            if (!SP._picSet[list[k]]) { out.push(list[k]); }
        }
        return out;
    };

    SP.canPlay = function(i) {
        return SP.missingOf(i).length === 0;
    };

    SP.checkAssets = function() {
        var bad = [];
        for (var i = 0; i < SCENES.length; i++) {
            var m = SP.missingOf(i);
            if (m.length) { bad.push('#' + SCENES[i].id + ' ' + SCENES[i].name + ' (缺' + m.length + ')'); }
        }
        var txt = bad.length
            ? ('缺素材场景 ' + bad.length + '/' + SCENES.length + '：\n' + bad.join('\n'))
            : ('全部 ' + SCENES.length + ' 个场景素材齐全');
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
        if (!SCENES.length) { SP.toast('场景列表为空'); return false; }
        i = Number(i);
        if (isNaN(i) || i < 0 || i >= SCENES.length) { return false; }
        var s = SCENES[i];
        if (!SP.canPlay(i)) {
            SP.toast('⚠ 跳过「' + s.name + '」：缺 Spicy Mod 素材');
            return false;
        }
        if (SP.busy()) { SP.toast('当前有事件/对话在运行，稍后再按'); return false; }
        SP.index = i;
        SP.last = i;
        $gameTemp.reserveCommonEvent(s.id);
        SP.playing = true;
        SP.grace = 20;
        SP.wait = AUTO_DELAY;
        SP.toast('▶ ' + (i + 1) + '/' + SCENES.length + '  ' + s.name + '  (#' + s.id + ')'
            + (SP.auto ? '   [自动连播]' : ''));
        return true;
    };

    SP.playId = function(id) {
        for (var i = 0; i < SCENES.length; i++) {
            if (SCENES[i].id === Number(id)) { return SP.play(i); }
        }
        // 不在列表里也允许直接播（无从预检素材）
        if (SP.busy()) { SP.toast('当前有事件/对话在运行，稍后再按'); return false; }
        $gameTemp.reserveCommonEvent(Number(id));
        SP.playing = true;
        SP.grace = 20;
        SP.toast('▶ 直接播放 #' + id);
        return true;
    };

    // 从 from 之后找第一个能播的（跳过缺素材的）
    SP.findPlayable = function(from) {
        var n = SCENES.length;
        for (var k = 1; k <= n; k++) {
            var i = ((from + k) % n + n) % n;
            if (SP.canPlay(i)) { return i; }
        }
        return -1;
    };

    SP.playNext = function() {
        if (!SCENES.length) { SP.toast('场景列表为空'); return false; }
        var i = SP.findPlayable(SP.last);
        if (i < 0) { SP.toast('没有可播放的场景（全部缺素材）'); return false; }
        return SP.play(i);
    };

    SP.playPrev = function() {
        if (!SCENES.length) { return false; }
        var n = SCENES.length;
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
        var s = (SP.last >= 0 && SCENES[SP.last]) ? SCENES[SP.last].name : '(未播放)';
        var txt = 'ScenePlayer: 共' + SCENES.length + '个 | 上次=' + s
            + ' | 连播=' + (SP.auto ? '开' : '关') + ' | 自动对话=' + (SP.msgAuto ? '开' : '关');
        console.log(txt);
        return txt;
    };

    SP.toast = function(text) {
        var scene = SceneManager._scene;
        if (scene && scene._spToast) { scene._spToast.show(text); }
        console.log('[ScenePlayer] ' + text);
    };

    SP.refreshHelp = function() {
        var scene = SceneManager._scene;
        if (scene && scene._helpWindow && scene.helpText) {
            scene._helpWindow.setText(scene.helpText());
        }
    };

    SP.update = function() {
        SP.updateAuto();
        SP.updateMessageAuto();
    };

    SP.updateAuto = function() {
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

    // 第 1 行：中文名（选中/上次播放会变色；缺素材会标 ⚠ 并变灰）
    // 第 2 行：英文原名（小字半透明；缺素材时改为显示缺了多少张）
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
        this.contents.fontSize = base;
        this.drawText(no + '  #' + it.id + '  ' + it.name + (miss.length ? '  ⚠缺素材' : ''),
            rect.x, rect.y, rect.width);
        var sub = miss.length ? ('缺 ' + miss.length + ' 张图，需 Spicy Mod：' + miss[0]) : it.orig;
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
        for (var i = 0; i < SP.scenes.length; i++) {
            if (!SP.canPlay(i)) { blocked++; }
        }
        return '↑↓ 选择   ←→ 跳10   PgUp/PgDn 翻页   Home/End 首尾   Enter 播放   Esc 关闭'
            + '     |     共 ' + SP.scenes.length + ' 个场景'
            + (blocked ? '（⚠ 缺素材 ' + blocked + ' 个，已跳过）' : '')
            + '    自动连播：' + (SP.auto ? '开' : '关')
            + '    自动对话：' + (SP.msgAuto ? '开' : '关');
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
        this._listWindow.setData(SP.scenes, SP.index);
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
        if (code !== KEY_OPEN && code !== KEY_NEXT && code !== KEY_AUTO && code !== KEY_MSG) { return; }
        var scene = SceneManager._scene;
        var inMap = (scene instanceof Scene_Map);
        var inList = (scene instanceof Scene_ScenePlayer);

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

    console.log('[ScenePlayer] v1.2.0 已加载，场景数 = ' + SCENES.length
        + '  | F7 列表  F8 下一个  F9 连播  F10 自动对话');
})();
