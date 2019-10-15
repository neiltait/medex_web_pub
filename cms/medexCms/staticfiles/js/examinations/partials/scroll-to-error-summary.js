(function ($) {

    function scrollToErrorSummary() {
        $('html, body').animate({
        scrollTop: $('#error_alert').offset().top
    }, 'slow');
    }

    $(document).on("page:load", scrollToErrorSummary)
    $(scrollToErrorSummary);

}(jQuery))
