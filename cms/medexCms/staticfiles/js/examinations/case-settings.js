(function ($) {

    var VoidCase = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    VoidCase.prototype = {
        setup: function () {
            this.confirmYes = this.wrapper.find('#void-yes');
            this.confirmNo = this.wrapper.find('#void-no');
            this.voidBtn = this.wrapper.find('.void-case-button');

            this.startWatchers();
        },

        startWatchers: function () {
            var that = this;

            this.confirmYes.click(function () {
                that.enableSubmitButton()
            });

            this.confirmNo.click(function () {
                that.disableSubmitButton()
            });
        },

        disableSubmitButton: function () {
            this.voidBtn.prop('disabled', true)
        },

        enableSubmitButton: function () {
            this.voidBtn.prop('disabled', false)
        }
    };

    function init() {
        var voidCaseWrapper = $('#void-case');
        new VoidCase(voidCaseWrapper)
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
