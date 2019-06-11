(function ($) {

    var AdditionalBereaved = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    AdditionalBereaved.prototype = {
        setup: function() {
            this.addBtn = this.wrapper.find('#add-another-btn');
            this.removeBtn = this.wrapper.find('#remove-btn');
            this.additionalShowing = 0;
            this.additionalBereaved = this.wrapper.find('.bereaved');
            this.representatives = [];
            this.initialiseRepresentatives();
            this.startWatchers();
            this.setInitialView();
        },

        setInitialView: function() {
            for (var i = 0; i < this.representatives.length; i++) {
                if(this.representatives[i].hasContent()) {
                    this.representatives[i].show();
                    this.additionalShowing++;
                    this.removeBtn.show();
                }
            }
        },

        initialiseRepresentatives: function() {
            for (var i = 0; i < this.additionalBereaved.length; i++) {
                this.representatives.push(new Representative(this.additionalBereaved[i]));
            }
        },

        startWatchers: function() {
            var that = this;
            this.addBtn.click(function() {
                that.representatives[that.additionalShowing].show();
                that.removeBtn.show();
                $(that.addBtn).text("Add another representative");
                that.additionalShowing++;

                if (that.additionalShowing === that.representatives.length) {
                  that.addBtn.hide();
                }
            });

            this.removeBtn.click(function() {
                that.additionalShowing--;
                that.addBtn.show();
                $(that.addBtn).text("Add representative");
                that.representatives[that.additionalShowing].hide();
                that.representatives[that.additionalShowing].clearContent();
                if (that.additionalShowing === 0) {
                    that.removeBtn.hide();
                }
            });
        }
    }

    var Representative = function(section) {
        this.section = $(section);
        this.setup();
    }

    Representative.prototype = {
        setup: function() {
            this.radioBtns = this.section.find('input[type=radio]');
            this.otherInputs = this.section.find('input:not([type=radio])');
        },

        hide: function() {
            this.section.hide();
        },

        show: function() {
            this.section.show();
        },

        hasContent: function() {
            return this.otherInputs[0].value !== '';
        },

        clearContent: function() {
            for (var i = 0; i < this.radioBtns.length; i++) {
                this.radioBtns[i].checked = false;
            }

            for (var i = 0; i < this.otherInputs.length; i++) {
                this.otherInputs[i].value = '';
                $(this.otherInputs[i]).trigger('change');
            }
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
