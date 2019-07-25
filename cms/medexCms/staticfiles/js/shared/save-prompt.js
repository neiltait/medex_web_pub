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

var SavePromptWithMultipleForms = function (forms) {
    this.forms = forms;
    this.submittedAsForm = false;
    this.content = [];
    this.prompt = "Are you sure you want to leave this page?";
    this.setup();
};

SavePromptWithMultipleForms.prototype = {
    setup: function () {

        for (var i = 0; i < this.forms.length; i++) {
            this.content.push(this.serializeIncludingDisabled(this.forms[i]))
            this.forms[i].submit(function (e) {
                this.submittedAsForm = true;
            });
        }
        this.bindWindow();
    },
    bindWindow: function () {
        var that = this;
        window.onbeforeunload = function (e) {
            if (!that.submittedAsForm) {
                for (var i = 0; i < that.forms.length; i++) {
                    if (that.content[i] !== that.serializeIncludingDisabled(that.forms[i])) {
                        e.returnValue = that.prompt;
                        return that.prompt
                    }
                }
            }
        }
    },

    serializeIncludingDisabled: function (form) {
        if(form) {
            var disabled = form.find(':input:disabled').removeAttr('disabled');
            var serialized = form.serialize();
            disabled.attr('disabled', 'disabled');
            return serialized
        } else {
            return ""
        }
    }
};