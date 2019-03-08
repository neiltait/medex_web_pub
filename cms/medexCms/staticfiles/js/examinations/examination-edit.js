(function ($) {

    var ExaminationEditForm = function (form) {
        this.form = $(form);
        this.setup();
    }

    ExaminationEditForm.prototype = {
        setup: function () {
            this.saveBar = this.form.find('.sticky-save');
            this.hasChanges = false;
            this.initialiseInputs();

            this.tab1 = this.form.find('#patient-details-tab');
            this.tab2 = this.form.find('#medical-team-tab');
            this.tab3 = this.form.find('#case-breakdown-tab');
            this.tab4 = this.form.find('#case-outcomes-tab');
            this.initialiseTabs();

            this.section1 = this.form.find('#patient-details-section');
            this.section2 = this.form.find('#medical-team-section');
            this.section3 = this.form.find('#case-breakdown-section');
            this.section4 = this.form.find('#case-outcomes-section');
        },

        initialiseTabs: function () {
            let that=this;
            this.tab1.click(function () { that.showTab("patient-details") });
            this.tab2.click(function () { that.showTab("medical-team") });
            this.tab3.click(function () { that.showTab("case-breakdown") });
            this.tab4.click(function () { that.showTab("case-outcomes") });
        },
        showTab: function(tabId) {
            for (tab of [this.tab1, this.tab2, this.tab3, this.tab4]) {
                if(tab[0].id === tabId + "-tab") {
                    tab.addClass("active")
                } else {
                    tab.removeClass("active")
                }
            }

            for (section of [this.section1, this.section2, this.section3, this.section4]) {
                if(section[0].id === tabId + "-section") {
                    section.removeClass("medex-hidden")
                } else {
                    section.addClass("medex-hidden")
                }
            }
        },
        initialiseInputs: function () {
            var inputs = this.form.find('input');
            for (var i = 0; i < inputs.length; i++) {
                new Input(inputs[i], this.handleChange.bind(this));
            }

            var selects = this.form.find('select');
            for (var i = 0; i < selects.length; i++) {
                new Input(selects[i], this.handleChange.bind(this));
            }

            var textAreas = this.form.find('textarea');
            for (var i = 0; i < textAreas.length; i++) {
                new Input(textAreas[i], this.handleChange.bind(this));
            }
        },

        handleChange: function () {
            this.hasChanges = true;
            this.showSave();
        },

        showSave: function () {
            this.saveBar.show();
        }
    }

    var Input = function (input, changeCallback) {
        this.input = $(input);
        this.changeCallback = changeCallback;
        this.setup();
    }

    Input.prototype = {
        setup: function () {
            this.startWatchers();
        },

        startWatchers: function () {
            this.input.change(this.changeCallback);

            this.input.on('input', this.changeCallback);
        }
    }

    function init() {
        var examinationsForms = $('#examination__edit--form');
        for (var i = 0; i < examinationsForms.length; i++) {
            new ExaminationEditForm(examinationsForms[i]);
        }
    }

    $(document).on('page:load', init);
    $(init)
}(jQuery))
