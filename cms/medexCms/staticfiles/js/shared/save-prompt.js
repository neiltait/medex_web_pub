var SavePromptForm = function (form) {
    this.form = form;
    this.submittedAsForm = false;
    this.content = "";
    this.prompt = "Are you sure you want to leave this page?";
    this.setup();
};

SavePromptForm.prototype = {
    setup: function () {
        if (this.form.length > 0) {
            this.content = this.serializeIncludingDisabled(this.form);
            var that = this;
            this.form.submit(function (e) {
                that.submittedAsForm = true;
            });
            this.bindWindow();
        }
    },
    bindWindow: function () {
        var that = this;
        window.onbeforeunload = function (e) {
            var newData = that.serializeIncludingDisabled(that.form);
            if (!that.submittedAsForm && (newData !== that.content)) {
                e.returnValue = that.prompt;
                return that.prompt
            }
        }
    },
    serializeIncludingDisabled: function (form) {
        var disabled = form.find(':input:disabled').removeAttr('disabled');
        var serialized = this.form.serialize();
        disabled.attr('disabled', 'disabled');
        return serialized

    }
};