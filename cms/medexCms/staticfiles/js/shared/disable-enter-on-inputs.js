(function ($) {

    function disableEnterOnInputs() {
        $(document).on("keydown", ":input:not(textarea):not(:submit)", function(event) {
            if (event.key == "Enter") {
                console.log("It's me again");
                event.preventDefault();
            }
        })
    }

    $(document).on("page:load", disableEnterOnInputs)
    $(disableEnterOnInputs);

}(jQuery))
