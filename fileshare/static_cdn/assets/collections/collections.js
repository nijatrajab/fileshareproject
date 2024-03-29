
// used exclusively to generate collections.min.js for browsers

requirejs.config({
    //Remember: only use shim config for non-AMD scripts,
    //scripts that do not already call define(). The shim
    //config will not work correctly if used on AMD scripts,
    //in particular, the exports and init config will not
    //be triggered, and the deps config will be confusing
    //for those cases.
    shim: {
        'backbone': {
            //These script dependencies should be loaded before loading
            //backbone.js
            deps: ['underscore', 'jquery'],
            //Once loaded, use the global 'Backbone' as the
            //module value.
            exports: 'Backbone'
        },
        'underscore': {
            exports: '_'
        },
        'foo': {
            deps: ['bar'],
            exports: 'Foo',
            init: function (bar) {
                //Using a function allows you to call noConflict for
                //libraries that support it, and do other cleanup.
                //However, plugins for those libraries may still want
                //a global. "this" for the function will be the global
                //object. The dependencies will be passed in as
                //function arguments. If this function returns a value,
                //then that value is used as the module export value
                //instead of the object found via the 'exports' string.
                //Note: jQuery registers as an AMD module via define(),
                //so this will not work for jQuery. See notes section
                //below for an approach for jQuery.
                return this.Foo.noConflict();
            }
        }
    }
});

//Then, later in a separate file, call it 'MyModel.js', a module is
//defined, specifying 'backbone' as a dependency. RequireJS will use
//the shim config to properly load 'backbone' and give a local
//reference to this module. The global Backbone will still exist on
//the page too.
define(['backbone'], function (Backbone) {
    return Backbone.Model.extend({});
});


var Shim = require("./shim");

/*jshint evil:true */
// reassigning causes eval to not use lexical scope.
var globalEval = eval,
    global = globalEval('this');
/*jshint evil:false */

global.List = require("./list");
global.Set = require("./set");
global.Map = require("./map");
global.MultiMap = require("./multi-map");
global.WeakMap = require("./weak-map");
global.SortedSet = require("./sorted-set");
global.SortedMap = require("./sorted-map");
global.LruSet = require("./lru-set");
global.LruMap = require("./lru-map");
global.SortedArray = require("./sorted-array");
global.SortedArraySet = require("./sorted-array-set");
global.SortedArrayMap = require("./sorted-array-map");
global.FastSet = require("./fast-set");
global.FastMap = require("./fast-map");
global.Dict = require("./dict");
global.Iterator = require("./iterator");

