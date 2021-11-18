require.async("second")
.then(function (second) {
    if (window.injectedScripts.length !== 1 || window.injectedScripts.every(function (src) {
        return src.search(/index\.html\.bundle-[0-9\-]\.js$/) !== -1;
    })) {
        window.error = "Expected a single bundle script to be loaded, instead got " + window.injectedScripts.join(", ");
    } else if (second !== 10) {
        window.error = "Second was not equal to 10";
    }
    window.done = true;
})
.done();

