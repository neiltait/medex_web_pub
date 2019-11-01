(function ($) {

    var CaseOutcomePage = function (wrapper) {
        this.wrapper = $(wrapper);
        this.setup();
    }

    CaseOutcomePage.prototype = {
        setup: function () {
            this.hasChanges = false;
            this.changedForm = null;
            this.scrutinyCompleteForm = new ScrutinyCompleteForm(this.wrapper.find('#scrutiny-form'),
                this.setHasChanges.bind(this));
            this.coronerReferralForm = new CoronerReferralForm(this.wrapper.find('#coroner-referral-form'),
                this.setHasChanges.bind(this));
            this.outstandingItemsForm = new OutstandingItemsForm(this.wrapper.find('#outstanding-items-form'),
                this.setHasChanges.bind(this));
            this.setupSavePromptForms();
        },

        setupSavePromptForms: function () {
            new SavePromptWithMultipleForms([this.wrapper.find('#scrutiny-form'),
                this.wrapper.find('#coroner-referral-form'),
                this.wrapper.find('#outstanding-items-form')]);
        },

        getHasChanges: function () {
            return this.hasChanges;
        },

        setHasChanges: function (value, form) {
            this.hasChanges = value;
            this.changedForm = form;
        },

        forceSave: function (nextTab) {
            this.changedForm.form[0].action += '?nextTab=' + nextTab;
            this.changedForm.form.submit();
        }
    }

    var ScrutinyCompleteForm = function (form, changeCallback) {
        this.form = $(form);
        this.changeCallback = changeCallback;
        this.setup();
    }

    ScrutinyCompleteForm.prototype = {
        setup: function () {
            this.checkBox = new Input(this.form.find('input#scrutiny-confirmation'), this.handleChange.bind(this));
            this.btn = this.form.find('button#confirm-scrutiny-button');

            this.setInitialView();
        },

        setInitialView: function () {
            this.btn.attr("disabled", true);
        },

        handleChange: function () {
            if (this.checkBox.isChecked()) {
                this.btn.attr("disabled", false);
                this.changeCallback(true, this);
            } else {
                this.btn.attr("disabled", true);
                this.changeCallback(false, null);
            }
        }
    }

    var CoronerReferralForm = function (form, changeCallback) {
        this.form = $(form);
        this.changeCallback = changeCallback;
        this.setup();
    }

    CoronerReferralForm.prototype = {
        setup: function () {
            this.checkBox = new Input(this.form.find('#coroner-referral-confirmation'), this.handleChange.bind(this));
            this.saveBar = this.form.find('.sticky-save');
        },

        handleChange: function () {
            if (this.checkBox.isChecked()) {
                this.toggleSaveBar();
                this.changeCallback(true, this);
            } else {
                this.toggleSaveBar();
                this.changeCallback(false, null);
            }
        },

        toggleSaveBar: function () {
            this.saveBar.toggle();
        }
    }

    var OutstandingItemsForm = function (form, changeCallback) {
        this.form = $(form);
        this.changeCallback = changeCallback;
        this.setup();
    }

    OutstandingItemsForm.prototype = {
        setup: function () {
            this.inputs = [];
            this.initialiseInputs();
            this.checkBox = new Input(this.form.find('#coroner-referral-confirmation'), this.handleChange.bind(this));
            this.saveBar = this.form.find('.sticky-save');
            this.showHideWaiveCremFee();
            this.waiveFeePanel = this.form.find("#waive-cremation-fee-decision");

            this.startWatchers();
        },

        initialiseInputs: function () {
            var inputsData = this.form.find('input');
            for (var i = 0; i < inputsData.length; i++) {
                this.inputs.push(new Input(inputsData[i], this.handleChange.bind(this)));
            }
        },

        handleChange: function () {
            this.showSaveBar();
            this.changeCallback(true, this);
        },

        showSaveBar: function () {
            this.saveBar.show();
        },

        showHideWaiveCremFee: function() {
            let selectedOutcome = this.form.find('input[name=cremation_form]:checked');
            if (selectedOutcome.length > 0 && selectedOutcome.val() === 'Yes') {
                console.log( this.waiveFeePanel)
                //this.waiveFeePanel.show();
            } else {
                console.log('says no')
                //this.waiveFeePanel.hide();
            }
        },

         startWatchers: function() {
            let that = this;
            $('input[type=radio][name=cremation_form]').change(function () {
                that.showHideWaiveCremFee();
            });
        }

    }

    function init() {
        var caseOutcome = $('.examination__edit');
        for (var i = 0; i < caseOutcome.length; i++) {
            new CaseOutcomePage(caseOutcome[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
