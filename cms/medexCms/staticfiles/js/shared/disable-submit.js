/*
    Ensures all forms with the class 'disabling-form' only submit once but disabling all submit buttons on form
    submission
 */

(function ($) {
    var SelfDisablingFormSet = function (forms) {
        this.forms = forms;
        this.setup()
    };

    SelfDisablingFormSet.prototype = {
        setup: function () {
            this.forms.one('submit', function () {
                $(this).find('input[type="submit"]').attr('disabled', 'disabled');
            });
        }
    };

    function init() {
        var disablingForms = $('.disabling-form');
        new SelfDisablingFormSet(disablingForms);
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery));
