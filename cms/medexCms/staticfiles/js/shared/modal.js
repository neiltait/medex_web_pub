(function ($) {

    var Popup = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    Popup.prototype = {
        setup: function () {
            this.cancelButton = this.wrapper.find('.modal-cancel-btn');

            this.startWatcher();
        },

        startWatcher: function() {
          var that = this;
          this.cancelButton.click(function(e) {
            that.wrapper.hide();
          });
        }
    }

    function init() {
        var popups = $('.medex-modal-cover');
        for (var i = 0; i < popups.length; i++) {
            new Popup(popups[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
