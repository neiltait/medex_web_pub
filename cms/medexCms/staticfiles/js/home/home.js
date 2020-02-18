(function ($) {

    var ExpandableCaseCard = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    ExpandableCaseCard.prototype = {
        setup: function() {
            this.upChevron = this.wrapper.find('.chevron-up');
            this.downChevron = this.wrapper.find('.chevron-down');
            this.caseHeader = this.wrapper.find('.case-card-header');
            this.caseBody = this.wrapper.find('.case-card-body');
            this.startWatchers();

            this.wrapper.attr('aria-expanded', 'false');
        },

        startWatchers: function() {
            var that = this;
            this.upChevron.click(function() {
                that.caseHeader.removeClass('case-card-header--expanded');
                that.caseBody.removeClass('case-card-body--expanded');

                that.wrapper.attr('aria-expanded', 'false');
            });

            this.downChevron.click(function() {
                that.caseHeader.addClass('case-card-header--expanded');
                that.caseBody.addClass('case-card-body--expanded');

                that.wrapper.attr('aria-expanded', 'true');
            });
        }
    }

    var FilterBlock = function(wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    FilterBlock.prototype = {
        setup: function() {
            this.form = this.wrapper.find('form');
            this.inputs = this.form.find('select');
            this.initialiseInputs();
        },

        initialiseInputs: function() {
            console.log(this)
            for (var i = 0; i < this.inputs.length; i++) {
                new FilterInput(this.inputs[i], this.submitForm.bind(this))
            }
        },

        submitForm: function() {
            this.form.submit();
        }
    }

    var FilterInput = function(input, callback) {
        this.input = $(input);
        this.changeCallback = callback
        this.setup();
    }

    FilterInput.prototype = {
        setup: function() {
            this.startWatcher();
        },

        startWatcher: function() {
            this.input.change(this.changeCallback);
        }
    }

    function init() {
        var indexFilters = $('#filter-block');
        new FilterBlock(indexFilters[0]);
        var caseCards = $('.case-card');
        for (var i = 0; i < caseCards.length; i++) {
            new ExpandableCaseCard(caseCards[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
