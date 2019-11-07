(function ($) {

    function scrollToErrorSummary() {
        var alert = $('#error_alert');
        if (alert.length > 0) {
            $('html, body').animate({
                scrollTop: alert.offset().top
            }, 'slow');
        }
    }

    $(document).on("page:load", scrollToErrorSummary)
    $(scrollToErrorSummary);

}(jQuery))
