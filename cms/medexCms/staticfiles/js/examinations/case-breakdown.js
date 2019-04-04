(function ($) {

    var EventEntryArea = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    EventEntryArea.prototype = {
        setup: function () {
            this.picker = this.wrapper.find('#event-form-picker');
            this.text = this.wrapper.find('#hidden-text');
            this.forms = {};
            this.activeForm = null;

            this.initialiseForms();
            this.startWatcher();
        },

        initialiseForms: function () {
            var forms = this.wrapper.find('.event-form');
            for (var i = 0; i < forms.length; i++) {
                var hintID = forms[i].id + '-hint';
                var hint = this.wrapper.find('#' + hintID)
                this.forms[forms[i].id] = new EventForm(forms[i], hint);
            }
        },

        startWatcher: function () {
            var that = this;
            this.picker.change(function (e) {
                that.forms[that.picker[0].value].show();
                that.hideOtherForms(that.picker[0].value);
                that.text.show();
            });
        },

        hideOtherForms: function (selectedKey) {
            if (this.activeForm) {
                this.forms[this.activeForm].hide();
                this.activeForm = selectedKey;
            } else {
                this.activeForm = selectedKey;
            }
        }
    }

    var EventForm = function (form, hint) {
        this.form = $(form);
        this.hint = $(hint);
        this.setup();
    }

    EventForm.prototype = {
        setup: function () {
            this.inputs = this.form.find('input');
        },

        show: function () {
            this.form.show();
            this.hint.show();
        },

        hide: function () {
            this.form.hide();
            this.hint.hide();
        }
    }

    var QAPDiscussionForm = function (form) {
        this.form = form;
        this.setup();
    };

    QAPDiscussionForm.prototype = {
        setup: function () {
            this.outcomeDecisionPanel = this.form.find("#qap-discussion__outcome-decision");
            this.revisedCauseOfDeathPanel = this.form.find("#qap-discussion__outcome-revised");
            this.showHideOutcome();
            this.showHideOutcomeDecision();

            this.startWatchers();
        },
        showHideOutcome() {
            let selectedOutcome = this.form.find('input[name=qap-discussion-outcome]:checked');
            if(selectedOutcome.length > 0 && selectedOutcome.val() === 'mccd') {
                this.outcomeDecisionPanel.show();
            } else {
                this.outcomeDecisionPanel.hide();
            }
        },
        showHideOutcomeDecision() {
            let selectedOutcomeDecision = this.form.find('input[name=qap-discussion-outcome-decision]:checked');
            if(selectedOutcomeDecision.length > 0 && selectedOutcomeDecision.val() !== 'outcome-decision-2') {
                this.revisedCauseOfDeathPanel.show();
            } else {
                this.revisedCauseOfDeathPanel.hide();
            }
        },
        startWatchers() {
            let that = this;
            $('input[type=radio][name=qap-discussion-outcome]').change(function () {
                if (this.value === 'mccd') {
                    that.outcomeDecisionPanel.show();
                } else {
                    that.outcomeDecisionPanel.hide();
                }
            });

            $('input[type=radio][name=qap-discussion-outcome-decision]').change(function () {
                if (this.value === 'outcome-decision-2') {
                    that.revisedCauseOfDeathPanel.hide();
                } else {
                    that.revisedCauseOfDeathPanel.show();
                }
            });
        }
    };


    var ChevronExpandable = function (wrapper) {
        this.wrapper = wrapper;
        this.setup();
    };

    ChevronExpandable.prototype = {
        setup() {
            this.header = this.wrapper.find(".expandable-header");
            this.body = this.wrapper.find(".expandable-body");
            this.upChevron = this.wrapper.find(".chevron-up");
            this.downChevron = this.wrapper.find(".chevron-down");

            this.startWatchers();
        },
        startWatchers() {
            let that = this;
            this.upChevron.click(function (e) {
                that.contract()
            });
            this.downChevron.click(function (e) {
                that.expand()
            });
        },
        expand() {
            this.header.addClass("expanded");
            this.body.addClass("expanded");
        },
        contract() {
            this.header.removeClass("expanded");
            this.body.removeClass("expanded");
        }
    };

    function init() {
        var eventEntry = $('.case-event-forms');
        for (var i = 0; i < eventEntry.length; i++) {
            new EventEntryArea(eventEntry[i]);
        }

        initQAPDiscussion();
        initBereavementDiscussion();
    }

    function initQAPDiscussion() {
        new QAPDiscussionForm($('#qap-discussion'));
        var causeOfDeath = new ChevronExpandable($('#qap-cause-of-death-panel'))
        causeOfDeath.expand();
    }

    var BereavementDiscussionForm = function (form) {
        this.form = form;
        this.setup();
    };

    BereavementDiscussionForm.prototype = {
        setup: function () {
//            this.outcomeDecisionPanel = this.form.find("#bereavement-discussion__outcome-decision");
//            this.showHideOutcome();
//            this.showHideOutcomeDecision();
//
//            this.startWatchers();
        },
        showHideOutcome() {
            let selectedOutcome = this.form.find('input[name=qap-discussion-outcome]:checked');
            if(selectedOutcome.length > 0 && selectedOutcome.val() === 'mccd') {
                this.outcomeDecisionPanel.show();
            } else {
                this.outcomeDecisionPanel.hide();
            }
        },
        showHideOutcomeDecision() {
            let selectedOutcomeDecision = this.form.find('input[name=qap-discussion-outcome-decision]:checked');
            if(selectedOutcomeDecision.length > 0 && selectedOutcomeDecision.val() !== 'outcome-decision-2') {
                this.revisedCauseOfDeathPanel.show();
            } else {
                this.revisedCauseOfDeathPanel.hide();
            }
        },
        startWatchers() {
            let that = this;
            $('input[type=radio][name=qap-discussion-outcome]').change(function () {
                if (this.value === 'mccd') {
                    that.outcomeDecisionPanel.show();
                } else {
                    that.outcomeDecisionPanel.hide();
                }
            });

            $('input[type=radio][name=qap-discussion-outcome-decision]').change(function () {
                if (this.value === 'outcome-decision-2') {
                    that.revisedCauseOfDeathPanel.hide();
                } else {
                    that.revisedCauseOfDeathPanel.show();
                }
            });
        }
    };


    function initBereavementDiscussion() {
        new BereavementDiscussionForm($('#bereavement-discussion'));
        var causeOfDeath = new ChevronExpandable($('#bereavement-cause-of-death-panel'))
        causeOfDeath.expand();
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
