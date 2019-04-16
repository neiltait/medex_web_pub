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
    },

    isChecked: function() {
        if (this.input[0].type === 'checkbox') {
            return this.input[0].checked;
        } else {
            console.error('Checked state being checked on a none checkbox input');
            return false
        }
    }
}