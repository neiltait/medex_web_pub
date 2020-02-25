(function ($) {

    function disableAutocompleteText() {
        $('input[type="text"]').attr("autocomplete", "off");
    }

    $(document).on("page:load", disableAutocompleteText)
    $(disableAutocompleteText);

}(jQuery))

