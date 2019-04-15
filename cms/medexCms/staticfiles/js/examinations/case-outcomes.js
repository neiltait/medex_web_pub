(function ($) {

    var ScrutinyCompleteForm = function (form) {
        this.form = $(form);
        this.setup();
    }

    ScrutinyCompleteForm.prototype = {
        setup: function () {
            this.checkBox = this.form.find('input#scrutiny-confirmation');
            this.btn = this.form.find('button#confirm-scrutiny-button');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            this.btn.attr("disabled", true);
        }

        startWatcher: function() {
            var that = this;
            this.checkBox.change(function() {
                if (that.checkBox[0].checked) {
                    that.btn.attr("disabled", false);
                } else {
                    that.btn.attr("disabled", true);
                }
            })
        }
    }

    function init() {
        var scrutinyForm = $('#scrutiny-form');
        for (var i = 0; i < scrutinyForm.length; i++) {
            new ScrutinyCompleteForm(scrutinyForm[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
