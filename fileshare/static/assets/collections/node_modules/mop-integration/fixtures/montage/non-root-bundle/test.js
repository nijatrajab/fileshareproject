var Montage = require("montage").Montage;

exports.Test = Montage.specialize({

    deserializedFromTemplate: {
        value: function () {
            if (this.pass !== true) {
                window.error = "pass was not set to true";
            }
            window.done = true;
        }
    }

});
