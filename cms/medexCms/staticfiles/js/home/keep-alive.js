(function ($) {

    var KeepAlive = function (input) {
        this.input = $(input);
        this.setup();
    };

    KeepAlive.prototype = {
        setup: function () {
            this.startWatcher();
        },

        startWatcher: function () {
            this.input.click(this.refreshTokens);
        },

        refreshTokens: function () {
            console.log("refreshing")
            $.ajax({
                url: "login-refresh",
                dataType: "json",
                method: "POST",
                context: document.body
            }).done(function () {
                console.log("done")
            });
        }
    };

    function init() {
        new KeepAlive("#test-button")
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery));
