/*
    Ensures all forms with the class 'disabling-form' only submit once but disabling all submit buttons on form
    submission
*/


(function ($) {

    function disableSubmit() {
        $('#examination__create--form').on('submit', function (event) {
            // 1. DEFAULT BEHAVIOUR = Submit form

            // 2. Change the handler to this form
            disableDefaultEvent();
        });
    }

    function disableDefaultEvent() {
        $('#examination__create--form').on('submit', function (event) {
            event.preventDefault();
        });
    }

    $(document).on('page:load', disableSubmit);
    $(disableSubmit)
}(jQuery));

