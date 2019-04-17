(function ($) {
    var RadioTogglePanelGroup = function (section) {
        this.section = section;
        this.setup()
    };

    RadioTogglePanelGroup.prototype = {
        setup: function () {
            this.radios = this.section.find(".radio-toggle-group__radio");
            this.panels = this.section.find(".radio-toggle-group__panel");
            this.setupWatchers();
            this.showHidePanels();
        },
        setupWatchers: function () {
            var that = this;
            this.radios.change(function () {
                that.showHidePanels()
            })
        },
        showHidePanels: function () {
            for (var i = 0; i < this.radios.length; i++) {
                if (this.radios[i].checked) {
                    this.panels[i].classList.remove('nhsuk-u-visually-hidden')
                } else {
                    this.panels[i].classList.add('nhsuk-u-visually-hidden')
                }
            }
        }
    };


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
                this.forms[forms[i].id] = new EventForm(forms[i], hint, this.setActiveForm.bind(this));
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
        },

        setActiveForm: function (formId) {
            this.activeForm = formId;
        }
    }

    var EventForm = function (form, hint, setActiveCallback) {
        this.form = $(form);
        this.hint = $(hint);
        this.setActiveCallback = setActiveCallback;
        this.setup();
    }

    EventForm.prototype = {
        setup: function () {
            this.inputs = this.form.find('input');
            this.setInitialView();
        },

        setInitialView: function () {
            if (this.form.hasClass('active')) {
                this.show();
                this.setActiveCallback(this.form[0].id)
            }
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
            if (selectedOutcome.length > 0 && selectedOutcome.val() === 'mccd') {
                this.outcomeDecisionPanel.show();
            } else {
                this.outcomeDecisionPanel.hide();
            }
        },
        showHideOutcomeDecision() {
            let selectedOutcomeDecision = this.form.find('input[name=qap-discussion-outcome-decision]:checked');
            if (selectedOutcomeDecision.length > 0 && selectedOutcomeDecision.val() !== 'outcome-decision-2') {
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
        var radioToggleGroups = $('.radio-toggle-group');
        for (var i = 0; i < radioToggleGroups.length; i++) {
            new RadioTogglePanelGroup(radioToggleGroups)
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
            this.newRep = this.form.find("#bereaved-new-rep");
            this.existingRep = this.form.find("#bereaved-existing-rep");
            this.repDetails = this.form.find("#bereaved-rep-details");
            this.repForm = this.form.find("#bereaved-rep-form");
            this.showHidePanels();

            this.startWatchers();

        },

        showHidePanels() {
            let selectedButton = this.form.find('input[name=bereaved-rep]:checked');
            if (selectedButton.val() === 'existing-rep') {
                this.repDetails.show();
                this.repForm.hide();
            } else {
                this.repForm.show();
                this.repDetails.hide();
            }
        },

        startWatchers() {
            let that = this;
            this.newRep.change(function () {
                that.showHidePanels();
            });

            this.existingRep.change(function () {
                that.showHidePanels();
            });
        }
    };


    function initBereavementDiscussion() {
        new BereavementDiscussionForm($('#bereaved-discussion'));
        var causeOfDeath = new ChevronExpandable($('#bereavement-cause-of-death-panel'))
        causeOfDeath.expand();
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
