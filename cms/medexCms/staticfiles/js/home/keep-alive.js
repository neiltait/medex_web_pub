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
            this.input.click(this.keepAlive.bind(this));
        },

        keepAlive: function () {
            var refreshCookie = this.readCookie("medex_do_not_refresh");

            if(!refreshCookie) {
                this.refreshTokens();
            }
        },

        refreshTokens: function () {
            $.ajax({
                url: "login-refresh",
                dataType: "json",
                method: "POST",
                context: document.body
            });
        },

        readCookie: function (name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        },
    };

    function init() {
        new KeepAlive("#test-button")
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery));
