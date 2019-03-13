(function ($) {

    var AdditionalBereaved = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    AdditionalBereaved.prototype = {
        setup: function () {
          this.addBtn = this.wrapper.find('#add-another-btn');
          this.removeBtn = this.wrapper.find('#remove-btn');
          this.additionalShowing = 0;
          this.additionalBereaved = this.wrapper.find('.bereaved');
          this.startWatchers();
        },

        startWatchers: function() {
          var that = this;
          this.addBtn.click(function() {
            $(that.additionalBereaved[that.additionalShowing]).show();
            that.removeBtn.show();
            that.additionalShowing++;
            if (that.additionalShowing === that.additionalBereaved.length) {
              that.addBtn.hide();
            }
          });

          this.removeBtn.click(function() {
            that.additionalShowing--;
            that.addBtn.show();
            $(that.additionalBereaved[that.additionalShowing]).hide();
            if (that.additionalShowing === 0) {
              that.removeBtn.hide();
            }
          });
        }
    }

    function init() {
        var additionalBereaved = $('.additional-bereaved');
        for (var i = 0; i < additionalBereaved.length; i++) {
            new AdditionalBereaved(additionalBereaved[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
