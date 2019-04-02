(function ($) {

    var TimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    TimelineEvent.prototype = {
        setup: function() {
            this.toggleBtn = this.eventBox.find('.event-toggle');
            this.contentSpace = this.eventBox.find('.event-body .content');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            if (this.contentSpace.height() > 56) {
                this.contentSpace.addClass('collapsed');
                this.toggleBtn.addClass('down');
            }
        },

        startWatcher: function() {
            var that = this;
            this.toggleBtn.click(function() {
                that.toggleContentShow();
            });
        },

        toggleContentShow: function() {
            this.toggleBtn.toggleClass('down');
            this.toggleBtn.toggleClass('up');
            this.contentSpace.toggleClass('collapsed')
        }
    }

    function init() {
        var events = $('.timeline-event');
        for (var i = 0; i < events.length; i++) {
            new TimelineEvent(events[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
