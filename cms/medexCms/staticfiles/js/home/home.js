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
        },

        startWatchers: function() {
            var that = this;
            this.upChevron.click(function() {
                that.caseHeader.removeClass('case-card-header--expanded');
                that.caseBody.removeClass('case-card-body--expanded');
            });

            this.downChevron.click(function() {
                that.caseHeader.addClass('case-card-header--expanded');
                that.caseBody.addClass('case-card-body--expanded');
            });
        }
    }

    function init() {
        var caseCards = $('.case-card');
        for (var i = 0; i < caseCards.length; i++) {
            new ExpandableCaseCard(caseCards[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
