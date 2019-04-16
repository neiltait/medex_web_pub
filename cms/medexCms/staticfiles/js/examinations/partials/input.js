var Input = function (input, changeCallback) {
    this.input = $(input);
    this.changeCallback = changeCallback;
    this.setup();
}

Input.prototype = {
    setup: function () {
        this.startWatchers();
    },

    startWatchers: function () {
        this.input.change(this.changeCallback);

        this.input.on('input', this.changeCallback);
    }
}