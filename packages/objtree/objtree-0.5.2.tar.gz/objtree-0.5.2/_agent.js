(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Agent = void 0;
var Agent = /** @class */ (function () {
    function Agent() {
        var _this = this;
        this.moduleBase = Process.enumerateModules()[0].base;
        this.cachedObjCResolver = null;
        this.cachedModuleResovler = null;
        this.objc_msgSend = null;
        this.stackDepth = 0;
        this.installedHooks = 0;
        this.pendingEvents = [];
        this.flushTimer = null;
        this.flush = function () {
            if (_this.flushTimer != null) {
                clearTimeout(_this.flushTimer);
                _this.flushTimer = null;
            }
            if (_this.pendingEvents.length == 0) {
                return;
            }
            send({
                type: 'events:add',
                message: _this.pendingEvents
            });
            _this.pendingEvents = [];
        };
    }
    Agent.prototype.init = function (spec, stackDepth) {
        this.stackDepth = stackDepth;
        try {
            this.start(spec);
            send({
                type: 'agent:finished_hooking',
                message: {
                    hooks: this.installedHooks,
                    depth: this.stackDepth
                }
            });
        }
        catch (e) {
            send({
                type: 'agent:error',
                message: e.message
            });
        }
    };
    Agent.prototype.start = function (spec) {
        this.objc_msgSend = Module.findExportByName(null, 'objc_msgSend');
        if (this.objc_msgSend == null) {
            throw new Error("Could not find objc_msgSend");
        }
        for (var _i = 0, spec_1 = spec; _i < spec_1.length; _i++) {
            var _a = spec_1[_i], key = _a[0], value = _a[1];
            switch (key) {
                case 'objc_method': {
                    this.installObjCHook(value);
                    break;
                }
                case 'function': {
                    this.installFunctionHook(value);
                    break;
                }
                case 'function_offset': {
                    this.installFunctionOffsetHook(value);
                    break;
                }
            }
        }
    };
    Agent.prototype.installObjCHook = function (pattern) {
        for (var _i = 0, _a = this.getObjCResolver().enumerateMatches(pattern); _i < _a.length; _i++) {
            var m = _a[_i];
            this.installHook(m.address, m.name);
        }
    };
    Agent.prototype.getObjCResolver = function () {
        var resolver = this.cachedObjCResolver;
        if (resolver == null) {
            try {
                resolver = new ApiResolver('objc');
            }
            catch (e) {
                throw new Error("Objective-C runtime is not available");
            }
            this.cachedObjCResolver = resolver;
        }
        return resolver;
    };
    Agent.prototype.installFunctionHook = function (pattern) {
        var q = parseModuleFunctionPattern(pattern);
        for (var _i = 0, _a = this.getModuleResolver().enumerateMatches("exports:" + q.module + "!" + q.function); _i < _a.length; _i++) {
            var m = _a[_i];
            this.installHook(m.address, m.name);
        }
    };
    Agent.prototype.getModuleResolver = function () {
        var resolver = this.cachedModuleResovler;
        if (resolver == null) {
            resolver = new ApiResolver('module');
            this.cachedModuleResovler = resolver;
        }
        return resolver;
    };
    Agent.prototype.installFunctionOffsetHook = function (offset) {
        var funcAbsoluteAddr = this.moduleBase.add(offset);
        this.installHook(funcAbsoluteAddr, "function at address " + funcAbsoluteAddr);
    };
    Agent.prototype.installHook = function (pointer, funcDescription) {
        var objc_msgSend = this.objc_msgSend;
        var agent = this;
        Interceptor.attach(pointer, {
            onEnter: function (args) {
                var originThreadId = this.threadId;
                //console.log("\n" + funcDescription);
                agent.emit([0, funcDescription]);
                this.hook = Interceptor.attach(objc_msgSend, {
                    onEnter: function (args) {
                        if (this.threadId == originThreadId) {
                            agent.objcOnEnter(this, args);
                        }
                    }
                });
            },
            onLeave: function (retval) {
                agent.emit([-1, '---------------------------------']); // Use depth -1 to mark the exiting of a function
                this.hook.detach();
            }
        });
        this.installedHooks++;
        send({
            type: 'agent:hook_installed',
            message: {
                target: funcDescription
            }
        });
    };
    Agent.prototype.objcOnEnter = function (ctx, args) {
        if (ctx.depth > this.stackDepth) {
            return;
        }
        var id = args[0];
        var selector = args[1].readCString();
        var cls;
        var typeQualifier;
        if (ObjC.api.object_isClass(id)) {
            typeQualifier = '+';
            cls = id;
        }
        else {
            typeQualifier = '-';
            cls = ObjC.api.object_getClass(id);
        }
        var clsName = ObjC.api.class_getName(cls).readCString();
        //console.log('|  '.repeat(ctx.depth) + `${typeQualifier}[${clsName} ${selector}]`);
        var objcMessage = typeQualifier + "[" + clsName + " " + selector + "]";
        this.emit([ctx.depth, objcMessage]);
    };
    // Credits for the following 3 funcs: https://github.com/frida/frida-tools/blob/master/agents/tracer/agent.ts
    Agent.prototype.emit = function (event) {
        this.pendingEvents.push(event);
        if (this.flushTimer == null) {
            this.flushTimer = setTimeout(this.flush, 50);
        }
    };
    return Agent;
}());
exports.Agent = Agent;
function parseModuleFunctionPattern(pattern) {
    var tokens = pattern.split("!", 2);
    var m, f;
    if (tokens.length === 1) {
        m = "*";
        f = tokens[0];
    }
    else {
        m = (tokens[0] === "") ? "*" : tokens[0];
        f = (tokens[1] === "") ? "*" : tokens[1];
    }
    return {
        module: m,
        function: f
    };
}

},{}],2:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var agent_1 = require("./agent");
var agent = new agent_1.Agent();
rpc.exports = {
    init: agent.init.bind(agent)
};

},{"./agent":1}]},{},[2])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJzcmMvYWdlbnQudHMiLCJzcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7Ozs7QUNHQTtJQUFBO1FBQUEsaUJBa0xDO1FBakxXLGVBQVUsR0FBRyxPQUFPLENBQUMsZ0JBQWdCLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUM7UUFDaEQsdUJBQWtCLEdBQXVCLElBQUksQ0FBQztRQUM5Qyx5QkFBb0IsR0FBdUIsSUFBSSxDQUFBO1FBQy9DLGlCQUFZLEdBQXlCLElBQUksQ0FBQztRQUMxQyxlQUFVLEdBQVcsQ0FBQyxDQUFDO1FBQ3ZCLG1CQUFjLEdBQUcsQ0FBQyxDQUFDO1FBQ25CLGtCQUFhLEdBQWlCLEVBQUUsQ0FBQztRQUNqQyxlQUFVLEdBQVEsSUFBSSxDQUFDO1FBeUp2QixVQUFLLEdBQUc7WUFDWixJQUFJLEtBQUksQ0FBQyxVQUFVLElBQUksSUFBSSxFQUFFO2dCQUN6QixZQUFZLENBQUMsS0FBSSxDQUFDLFVBQVUsQ0FBQyxDQUFDO2dCQUM5QixLQUFJLENBQUMsVUFBVSxHQUFHLElBQUksQ0FBQzthQUMxQjtZQUVELElBQUksS0FBSSxDQUFDLGFBQWEsQ0FBQyxNQUFNLElBQUksQ0FBQyxFQUFFO2dCQUNoQyxPQUFPO2FBQ1Y7WUFFRCxJQUFJLENBQUM7Z0JBQ0QsSUFBSSxFQUFFLFlBQVk7Z0JBQ2xCLE9BQU8sRUFBRSxLQUFJLENBQUMsYUFBYTthQUM5QixDQUFDLENBQUM7WUFFSCxLQUFJLENBQUMsYUFBYSxHQUFHLEVBQUUsQ0FBQztRQUM1QixDQUFDLENBQUM7SUFDTixDQUFDO0lBeEtHLG9CQUFJLEdBQUosVUFBSyxJQUFjLEVBQUUsVUFBa0I7UUFDbkMsSUFBSSxDQUFDLFVBQVUsR0FBRyxVQUFVLENBQUM7UUFFN0IsSUFBSTtZQUNBLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7WUFDakIsSUFBSSxD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
