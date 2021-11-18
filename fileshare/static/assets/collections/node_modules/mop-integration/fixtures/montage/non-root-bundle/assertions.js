var Q = require("q");

// PhantomJS doesn't support all the ES5 features Montage
// needs, and so we can only test the mopping, not that it
// actually runs
exports.shouldTestInBrowser = false;

exports.run = function (fs, buildPath) {
    return Q.all([
        fs.read(fs.join(buildPath, "sub", "index.html.bundle-1-0.js"))
        .then(function (content) {
            content = content.toString("utf8");
            if (content.indexOf('bundleLoaded("index.html.bundle-1-0.js")') === -1) {
                return "incorrect bundleLoaded call";
            }
        })
    ]);
};
