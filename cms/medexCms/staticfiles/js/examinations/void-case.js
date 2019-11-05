(function ($) {

    var VoidCase = function (wrapper) {
        this.wrapper = wrapper
        this.setup();
    }

    VoidCase.prototype = {
        setup: function () {
            this.reasonSection = this.wrapper.find('#void-case-reason');
            this.confirmYes = this.wrapper.find('#void-yes');
            this.confirmNo = this.wrapper.find('#void-no');
            this.voidBtn = this.wrapper.find('.void-case')

            this.startWatchers();
        },

        startWatchers: function () {
            var that = this;

            this.confirmYes.click(function () {
                that.enableVoidButton()
            });
        },


        enableVoidButton: function () {
            this.enableSubmitButton()
        },

        disableVoidButton: function () {
            this.disableSubmitButton()
        },

        disableSubmitButton: function () {
            this.voidBtn.prop('disabled', true)
        },

        enableSubmitButton: function () {
            this.voidBtn.prop('disabled', false)
            console.log(this.voidBtn)
        }
    };

    function init() {
        var voidCaseWrapper = $('#void-case');
        VoidCase(voidCaseWrapper)
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))