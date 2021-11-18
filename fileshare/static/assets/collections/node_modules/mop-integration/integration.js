#!/usr/bin/env node

var spawn = require("child_process").spawn;
var FS = require("q-io/fs");
var PATH = require("path");
var Q = require("q");
var temp = require('temp');
require('colors');

var exec = require("./lib/exec");
var install = require("./lib/install");
var fixturesFor = require("./lib/fixtures-for").fixturesFor;
var test = require("./lib/test");

process.on('uncaughtException', function (error) {
    console.error("uncaughtException", error);
    console.error("stack", error.stack);
    throw error;
});

// FIXME: Q 0.9.6 uses process.nextTick and exceeds the maxTickDepth when
// mopping Montage. As a temporary fix increase the limit.
// Remove when Q uses setImmediate instead.
process.maxTickDepth = 5000;

global.DEBUG = process.env.DEBUG === "true";
var TIMEOUT = 10000;

var MOP_VERSION = process.env.MOP_VERSION,
    MR_VERSION = process.env.MR_VERSION,
    MONTAGE_VERSION = process.env.MONTAGE_VERSION;

if (!MOP_VERSION) {
    throw new Error("MOP_VERSION must be set");
}
if (MR_VERSION && MONTAGE_VERSION) {
    throw new Error("MR_VERSION and MONTAGE_VERSION may not be set at the same time");
}
if (!MR_VERSION && !MONTAGE_VERSION) {
    throw new Error("One of MR_VERSION and MONTAGE_VERSION must be set");
}

var projectName, projectVersion;
if (MR_VERSION) {
    projectName = "mr";
    projectVersion = MR_VERSION;
} else {
    projectName = "montage";
    projectVersion = MONTAGE_VERSION;
}

console.log("Testing mop and " + projectName);

var tempDir = temp.mkdirSync('mop-integration');
FS.copyTree(PATH.join(__dirname, "fixtures"), tempDir)
.then(function () {
    return install("mop", MOP_VERSION, tempDir)
    .then(function () {
        var optimize = require(PATH.join(tempDir, "node_modules", "mop"));
        // Get fixtures depending on runtime
        var fixturesPath = PATH.join(tempDir, projectName);
        return FS.list(fixturesPath)
        .then(function (names) {
            var failed = false;
            return names.reduce(function (previous, name) {
                var dir = PATH.join(fixturesPath, name);
                return previous.then(function () {
                    // install Mr/Montage
                    return install(projectName, projectVersion, dir);
                })
                .then(function () {
                    return test(optimize, projectName, name, FS, dir);
                })
                .then(function (errorMessages) {
                    if (errorMessages && errorMessages.length !== 0) {
                        console.log((name + " failed: \n" + errorMessages.join('\n')).red);
                        failed = true;
                    } else {
                        console.log((name + " passed").green);
                    }
                    console.log();
                });
            }, Q())
            .then(function () {
                if (failed) {
                    throw new Error("Test failed");
                }
            });
        });
    });
}).catch(function (err) {
    console.log(err);
    process.exit(1);
});
