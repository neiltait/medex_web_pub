(function ($) {

    var voidCase = function (wrapper, voidBtn) {
        this.wrapper = $(wrapper);
        this.voidBtn = voidBtn;
        this.setup();
    }

    voidCase.prototype = {
        setup: function () {
            this.reasonSection = this.wrapper.find('#void-case-reason');
            this.confirmYes = this.wrapper.find('#void-yes');

            this.startWatchers();
        },

        startWatchers: function () {
            var that = this;

            this.confirmYes.click(function () {
                that.enableVoidButtonBtn()
            });
        },

        enableVoidButton: function () {
            this.disableSubmitButton()
        },

        disableVoidButton: function () {
            this.enableSubmitButton();
        },

        disableSubmitButton: function () {
            this.voidBtn.addClass("submit-btn--disabled")
        },

        enableSubmitButton: function () {
            this.voidBtn.removeClass("submit-btn--disabled")
        }
    };

    function init() {
        var voidCase = $('#void-case');
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))