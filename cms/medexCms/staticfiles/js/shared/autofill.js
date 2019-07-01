(function ($) {

    function disableAutocompleteText() {
        $('input[type="text"]').attr("autocomplete", "none");

    }

    $(document).on("page:load", disableAutocompleteText)
    $(disableAutocompleteText);

}(jQuery))

