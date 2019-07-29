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
            this.picker = this.wrapper.find('select#event-form-picker ');
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
            this.picker[0].value = formId;
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
                this.setActiveCallback(this.form[0].id);
                this.form[0].scrollIntoView({
                    behavior: "smooth",
                });
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
            this.coronerDecisionPanel = this.form.find("#qap-discussion__coroner-decision");
            this.revisedCauseOfDeathPanel = this.form.find("#qap-discussion__outcome-revised");
            this.showHideOutcome();
            this.showHideOutcomeDecision();

            this.startWatchers();
        },

        showHideOutcome: function() {
            let selectedOutcome = this.form.find('input[name=qap-discussion-outcome]:checked');

            if (selectedOutcome.length > 0 && selectedOutcome.val() === 'IssueAnMccd') {
                this.outcomeDecisionPanel.show();
                this.coronerDecisionPanel.hide();
            } else if (selectedOutcome.length > 0 && selectedOutcome.val() === 'ReferToCoroner') {
                this.outcomeDecisionPanel.hide();
                this.coronerDecisionPanel.show();
            } else {
                this.outcomeDecisionPanel.hide();
                this.coronerDecisionPanel.hide();
            }
        },

        showHideOutcomeDecision: function() {
            let selectedOutcomeDecision = this.form.find('input[name=qap-discussion-outcome-decision]:checked');
            let selectedOutcome = this.form.find('input[name=qap-discussion-outcome]:checked');
            if (selectedOutcome.length > 0 && selectedOutcome.val() === 'ReferToCoroner') {
                this.revisedCauseOfDeathPanel.hide();
            }
            else if (selectedOutcomeDecision.length > 0 && selectedOutcomeDecision.val() !== 'MccdCauseOfDeathProvidedByME') {
                this.revisedCauseOfDeathPanel.show();
            }
            else {
                this.revisedCauseOfDeathPanel.hide();
            }
        },

        startWatchers: function() {
            let that = this;
            $('input[type=radio][name=qap-discussion-outcome]').change(function () {
                if (this.value === 'IssueAnMccd') {
                    that.outcomeDecisionPanel.show();
                    that.coronerDecisionPanel.hide();
                } else {
                    that.coronerDecisionPanel.show();
                    that.outcomeDecisionPanel.hide();
                }

                that.showHideOutcomeDecision();
            });

            $('input[type=radio][name=qap-discussion-outcome-decision]').change(function () {
                if (this.value === 'MccdCauseOfDeathProvidedByME') {
                    that.revisedCauseOfDeathPanel.hide();
                } else {
                    that.revisedCauseOfDeathPanel.show();
                }
            });
        }
    };

    var PreScrutinyForm = function (form) {
        this.form = form;
        this.setup();
    };

    PreScrutinyForm.prototype = {
        setup: function () {
            this.coronerDecisionPanel = this.form.find("#pre-scrutiny__coroner-decision");
            this.showHideCoronerPanel();

            this.startWatchers();
        },

        showHideCoronerPanel: function() {
            let selectedOutcome = this.form.find('input[name=ops]:checked');

            if (selectedOutcome.length > 0 && selectedOutcome.val() === 'ReferToCoroner') {
                this.coronerDecisionPanel.show();
            } else {
                this.coronerDecisionPanel.hide();
            }
        },

        startWatchers: function() {
            let that = this;
            $('input[type=radio][name=ops]').change(function () {
                if (this.value === 'IssueAnMccd') {
                    that.coronerDecisionPanel.hide();
                } else {
                    that.coronerDecisionPanel.show();
                }
            });
        }
    };

    var ChevronExpandable = function (wrapper) {
        this.wrapper = wrapper;
        this.setup();
    };

    ChevronExpandable.prototype = {
        setup: function() {
            this.header = this.wrapper.find(".expandable-header");
            this.body = this.wrapper.find(".expandable-body");
            this.upChevron = this.wrapper.find(".chevron-up");
            this.downChevron = this.wrapper.find(".chevron-down");

            this.startWatchers();
        },

        startWatchers: function() {
            let that = this;
            this.upChevron.click(function (e) {
                that.contract()
            });
            this.downChevron.click(function (e) {
                that.expand()
            });
        },

        expand: function() {
            this.header.addClass("expanded");
            this.body.addClass("expanded");
        },
        contract: function() {
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

        var mainForm = $('.form');
        new SavePromptForm(mainForm);

        initPreScrutiny();
        initQAPDiscussion();
        initBereavementDiscussion();
        initLatestAdmissionForm();
    }


    function initPreScrutiny() {
        new PreScrutinyForm($('#pre-scrutiny'));
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
            this.noRep = this.form.find("#bereaved-no-rep");
            this.repDetails = this.form.find("#bereaved-rep-details");
            this.repForm = this.form.find("#bereaved-rep-form");
            this.unableCheckbox = this.form.find("#bereaved-discussion-could-not-happen");
            this.dayOfConversation = this.form.find("#doc-day");
            this.monthOfConversation = this.form.find("#doc-month");
            this.yearOfConversation = this.form.find("#doc-year");
            this.timeOfConversation = this.form.find("#doc-time");
            this.discussionDetails = this.form.find("#bereavement-discussion-details");

            this.showHideRepTypePanels();

            this.concernsRadio = this.form.find("#bereavment-discussion-outcome-concerns");
            this.noConcernsRadio = this.form.find("#bereavement-discussion-outcome-no-concerns");
            this.concernsPanel = this.form.find("#bereavement-discussion-concerned-outcomes");
            this.showHideConcernsPanel();
            this.enableOrDisableAllControls();

            this.startWatchers();
        },

        showHideRepTypePanels: function() {
            let selectedButton = this.form.find('input[name=bereaved_rep_type]:checked');
            if (selectedButton.val() === 'bereaved-representative') {
                this.repDetails.show();
                this.repForm.hide();
            } else if (selectedButton.val() === 'nobody') {
                this.repDetails.hide();
                this.repForm.hide();
            } else {
                this.repForm.show();
                this.repDetails.hide();
            }
        },

        showHideConcernsPanel: function() {
            let selectedButton = this.form.find('input[name=bereaved_discussion_outcome]:checked');
            if (selectedButton && (selectedButton.val() === 'concerns')) {
                this.concernsPanel.show();
            } else {
                this.concernsPanel.hide();
            }
        },

        startWatchers: function() {
            let that = this;
            this.newRep.change(function () {
                that.showHideRepTypePanels();
            });

            this.existingRep.change(function () {
                that.showHideRepTypePanels();
            });

            this.noRep.change(function () {
                that.showHideRepTypePanels();
            });

            this.concernsRadio.change(function () {
                that.showHideConcernsPanel();
            });

            this.noConcernsRadio.change(function () {
                that.showHideConcernsPanel()
            });

            this.unableCheckbox.change(function() {
                that.enableOrDisableAllControls();
            })
        },

        enableOrDisableAllControls: function() {
            let that = this;
            var disable = this.unableCheckbox.prop('checked');
            this.dayOfConversation[0].disabled = disable;
            this.monthOfConversation[0].disabled = disable;
            this.yearOfConversation[0].disabled = disable;
            this.timeOfConversation[0].disabled = disable;
            this.discussionDetails[0].disabled = disable;
            this.noConcernsRadio[0].disabled = disable;
            this.concernsRadio[0].disabled = disable;

        }
    };


    function initBereavementDiscussion() {
        new BereavementDiscussionForm($('#bereaved-discussion'));
        var causeOfDeath = new ChevronExpandable($('#bereavement-cause-of-death-panel'))
        causeOfDeath.expand();
    }

    var LatestAdmissionCheckboxGroup = function (textboxes, checkbox) {
        this.textboxes = textboxes;
        this.checkbox = checkbox;
        this.setup();
    };

    LatestAdmissionCheckboxGroup.prototype = {
        setup: function () {
            this.setupCheckboxHandler();
            this.enabledOrDisable();
            this.setupTextboxesHandler();
        },

        setupCheckboxHandler: function () {
            var that = this;
            this.checkbox.change(
                function () {
                    $.each(that.textboxes, function (index, textInput) {

                        if (that.checkbox.prop('checked')) {
                            textInput[0].disabled = true
                        } else {
                            textInput[0].disabled = false
                        }
                    });
                }
            );
        },

        enabledOrDisable: function () {
            var that = this;
            if (this.checkbox.prop('checked')) {
                $.each(that.textboxes, function (index, textInput) {
                    textInput[0].disabled = true
                })
            } else {
                var textboxesAreEmpty = true;
                $.each(that.textboxes, function (index, textInput) {
                    if(textInput.val() !== '') {
                        textboxesAreEmpty = false;
                    }
                });
                if(textboxesAreEmpty === false) {
                    that.checkbox.prop("disabled", true);
                }
            }
        },

        setupTextboxesHandler: function () {
        var that = this;
        for (var i = 0; i < that.textboxes.length; i++) {
            that.textboxes[i].on('change keyup paste mouseup', function () {
                that.checkbox.prop("disabled", that.anyTextBoxesHaveContent(that.textboxes));
            })
        }
    },

        anyTextBoxesHaveContent: function () {
            for (var i = 0; i < this.textboxes.length; i++) {
                if (this.textboxes[i].val() !== '') {
                    return true
                }
            }
            return false
        },

    };



    var LatestAdmissionForm = function (form) {
        this.form = form;
        this.setup();
    };

    LatestAdmissionForm.prototype = {
        setup: function () {
            this.dateGroup = new LatestAdmissionCheckboxGroup([this.form.find("#day_of_last_admission"), this.form.find("#month_of_last_admission"), this.form.find("#year_of_last_admission")], this.form.find("#date_of_last_admission_not_known"));
            this.timeGroup = new LatestAdmissionCheckboxGroup([this.form.find("#time_of_last_admission")], this.form.find("#time_of_last_admission_not_known"));
            this.inputGroups = [this.dateGroup, this.timeGroup];
            this.initialiseFormWithData();
    },

    initialiseFormWithData: function() {
        for(var i = 0; i < this.inputGroups.length; i++) {
            this.inputGroups[i].enabledOrDisable();
        }
    },


  }

   function initLatestAdmissionForm() {
        new LatestAdmissionForm($('#admin-notes'));
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
