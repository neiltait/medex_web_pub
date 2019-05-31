(function ($) {

    var Timeline = function(timeline) {
        this.timeline = $(timeline);
        this.setup();
    }

    Timeline.prototype = {
        setup: function() {
            console.info('initialising timeline');
            this.initialEvent = new InitialTimelineEvent(this.timeline.find('.timeline-event-row.initial'));
            this.initialisePreScrutinyEvents();
            this.initialiseBereavedEvents();
            this.initialiseAdmissionEvents();
            this.initialiseQAPEvents();
            this.initialiseStandardEvents();
        },

        initialisePreScrutinyEvents: function() {
            this.preScrutinyEvents = []
            var preScrutinyEvents = this.timeline.find('.timeline-event-row.pre-scrutiny');
            for (var i = 0; i < preScrutinyEvents.length; i++) {
                this.preScrutinyEvents.push(new PreScrutinyTimelineEvent(preScrutinyEvents[i]));
            }
        },

        initialiseBereavedEvents: function() {
            this.bereavedEvents = []
            var bereavedEvents = this.timeline.find('.timeline-event-row.bereaved-discussion');
            for (var i = 0; i < bereavedEvents.length; i++) {
                this.bereavedEvents.push(new BereavedTimelineEvent(bereavedEvents[i]));
            }
        },

        initialiseAdmissionEvents: function() {
            this.admissionEvents = []
            var admissionEvents = this.timeline.find('.timeline-event-row.admission-notes');
            for (var i = 0; i < admissionEvents.length; i++) {
                this.admissionEvents.push(new AdmissionTimelineEvent(admissionEvents[i]));
            }
        },

        initialiseQAPEvents: function() {
            this.qapEvents = []
            var qapEvents = this.timeline.find('.timeline-event-row.qap-discussion');
            for (var i = 0; i < qapEvents.length; i++) {
                this.qapEvents.push(new QAPTimelineEvent(qapEvents[i]));
            }
        },

        initialiseStandardEvents: function() {
            this.otherEvents = []
            var otherEvents = this.timeline.find('.timeline-event-row.other');
            for (var i = 0; i < otherEvents.length; i++) {
                this.otherEvents.push(new StandardTimelineEvent(otherEvents[i]));
            }

            this.medicalHistoryEvents = []
            var medicalHistoryEvents = this.timeline.find('.timeline-event-row.medical-history');
            for (var i = 0; i < medicalHistoryEvents.length; i++) {
                this.medicalHistoryEvents.push(new StandardTimelineEvent(medicalHistoryEvents[i]));
            }

            this.meoSummaryEvents = []
            var meoSummaryEvents = this.timeline.find('.timeline-event-row.meo-summary');
            for (var i = 0; i < meoSummaryEvents.length; i++) {
                this.meoSummaryEvents.push(new StandardTimelineEvent(meoSummaryEvents[i]));
            }
        }
    }

    var InitialTimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    InitialTimelineEvent.prototype = {
        setup: function() {
            console.info('initialising Initial event');
        }
    }

    var PreScrutinyTimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    PreScrutinyTimelineEvent.prototype = {
        setup: function() {
            this.toggleBtn = this.eventBox.find('.event-toggle');
            this.contentSpace = this.eventBox.find('.event-body .content');
            this.details = this.eventBox.find('.event-body .content .details-body');
            this.hideableSection = this.eventBox.find('.event-body .content .hideable-content');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            if (this.contentSpace.height() > 56) {
                this.details.addClass('collapsed');
                this.toggleBtn.addClass('down');
                this.hideableSection.hide();
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
            this.details.toggleClass('collapsed');
            this.hideableSection.toggle();
        }
    }

    var BereavedTimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    BereavedTimelineEvent.prototype = {
       setup: function() {
            this.toggleBtn = this.eventBox.find('.event-toggle');
            this.contentSpace = this.eventBox.find('.event-body .content');
            this.details = this.eventBox.find('.event-body .content .details-body');
            this.hideableSection = this.eventBox.find('.event-body .content .hideable-content');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            if (this.contentSpace.height() > 56) {
                this.details.addClass('collapsed');
                this.toggleBtn.addClass('down');
                this.hideableSection.hide();
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
            this.details.toggleClass('collapsed');
            this.hideableSection.toggle();
        }
    }

    var AdmissionTimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    AdmissionTimelineEvent.prototype = {
        setup: function() {
            this.toggleBtn = this.eventBox.find('.event-toggle');
            this.hideableSection = this.eventBox.find('.event-body .content .hideable-content');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            this.toggleBtn.addClass('down');
            this.hideableSection.hide();
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
            this.hideableSection.toggle();
        }
    }

    var QAPTimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    QAPTimelineEvent.prototype = {
        setup: function() {
            this.toggleBtn = this.eventBox.find('.event-toggle');
            this.hideableSection = this.eventBox.find('.event-body .content .hideable-content');

            this.setInitialView();
            this.startWatcher();
        },

        setInitialView: function() {
            this.toggleBtn.addClass('down');
            this.hideableSection.hide();
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
            this.hideableSection.toggle();
        }
    }

    var StandardTimelineEvent = function(eventBox) {
        this.eventBox = $(eventBox);
        this.setup();
    }

    StandardTimelineEvent.prototype = {
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
        var timeline = $('.case-timeline');
        for (var i = 0; i < timeline.length; i++) {
            new Timeline(timeline[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
