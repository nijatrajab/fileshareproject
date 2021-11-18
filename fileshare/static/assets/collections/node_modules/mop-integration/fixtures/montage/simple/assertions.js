var Q = require("q");
var path = require("path");

// PhantomJS doesn't support all the ES5 features Montage
// needs, and so we can only test the mopping, not that it
// actually runs
exports.shouldTestInBrowser = false;

exports.run = function (fs, buildPath) {
    return Q.all([
        fs.stat(path.join(buildPath))
        .then(function (stat) {
            if (!stat.isDirectory()) {
                return "Build directory not created";
            }
        })
    ]);
};
