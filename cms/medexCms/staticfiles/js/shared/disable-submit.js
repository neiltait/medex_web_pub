/*
    Ensures all forms with the class 'disabling-form' only submit once but disabling all submit buttons on form
    submission
*/


(function ($) {

    function disableSubmit() {
        $('#examination__create--form').one('submit', function (event) {
                event.preventDefault();
                $('input[type="submit"]').submit();
        });
    }

    $(document).on('page:load', disableSubmit);
    $(disableSubmit)
}(jQuery));

