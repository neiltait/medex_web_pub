var SavePromptForm = function (form) {
    this.form = form;
    this.submittedAsForm = false;
    this.content = "";
    this.prompt = "Are you sure you want to leave this page?";
    this.setup();
};

SavePromptForm.prototype = {
    setup: function () {
        this.content = this.form.serialize()
        that = this;
        this.form.submit(function (e) {
            that.submittedAsForm = true;
        });
        this.bindWindow();
    },
    bindWindow: function () {
        var that = this;
        window.onbeforeunload = function (e) {
            var newData = that.form.serialize();
            if (!that.submittedAsForm && (newData !== that.content)) {
                e.returnValue = that.prompt;
                return that.prompt
            }
        }
    }
};