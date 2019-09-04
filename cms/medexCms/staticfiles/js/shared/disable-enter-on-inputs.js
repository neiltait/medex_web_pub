(function ($) {

    function disableEnterOnInputs() {
        $(document).on("keydown", ":input:not(textarea):not(:submit)", function(event) {
            if (event.key == "Enter") {
                event.preventDefault();
            }
        })
    }

    $(document).on("page:load", disableEnterOnInputs)
    $(disableEnterOnInputs);

}(jQuery))
