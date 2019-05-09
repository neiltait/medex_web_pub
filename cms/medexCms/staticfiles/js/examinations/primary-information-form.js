let REQUIRED_PLACEHOLDER = "Required";


var Form = function (form) {
    this.showValidation = false;
    this.visibleHospitalNumbers = 1;
    this.form = form;
    this.setup();
};

Form.prototype = {
    setup: function () {
        this.inputGroups = [];
        this.inputGroups.push(new TextInputsCheckboxGroup([this.form.find("#nhs_number")], this.form.find("#nhs_number_not_known")));
        this.inputGroups.push(new TextInputsCheckboxGroup([this.form.find("#time_of_death")], this.form.find("#time_of_death_not_known")));
        this.inputGroups.push(new TextInputsCheckboxGroup([this.form.find("#day_of_death"), this.form.find("#month_of_death"), this.form.find("#year_of_death")], this.form.find("#date_of_death_not_known")));
        this.inputGroups.push(new TextInputsCheckboxGroup([this.form.find("#day_of_birth"), this.form.find("#month_of_birth"), this.form.find("#year_of_birth")], this.form.find("#date_of_birth_not_known")));

        this.surnameInput = this.form.find("#last_name");
        this.givenNameInput = this.form.find("#first_name");
        this.setupGivenNameInput();
        this.setupSurnameInput();

        this.hospitalNumber1 = this.form.find("#hospital_number_1");
        this.hospitalNumber1Textbox = this.form.find("#hospital_number_1_textbox");
        this.hospitalNumber1Label = this.form.find("#hospital_number_1_label");
        this.hospitalNumber2 = this.form.find("#hospital_number_2");
        this.hospitalNumber2Textbox = this.form.find("#hospital_number_2_textbox");
        this.hospitalNumber3 = this.form.find("#hospital_number_3");
        this.hospitalNumber3Textbox = this.form.find("#hospital_number_3_textbox");
        this.hospitalNumberAddBtn = this.form.find("#hospital-number__add-btn");
        this.setupHospitalNumberAddBtn();

        this.genderRadioButtons = this.form.find('input[type=radio][name=gender]');

        this.genderDetailArea = this.form.find("#more-gender-detail-area")
        this.genderDetailTextbox = this.form.find("#more-gender");
        this.genderMale = this.form.find('#gender-1');
        this.genderFemale = this.form.find('#gender-2');
        this.genderOther = this.form.find('#gender-3');

        this.setupGenderRadioButtons();

        this.placeOfDeathSelect = this.form.find('#place_of_death');
        this.placeOfDeathDropdown = this.form.find('#place_of_death_dropdown');
        this.setupPlaceOfDeath();

        this.meOfficeSelect = this.form.find('#me_office');
        this.meOfficeDropdown = this.form.find('#me_office_dropdown');
        this.setupMeOffice();

        this.submitButton = this.form.find("#submit-btn");
        this.setupSubmitButton();

        this.errorAlert = this.form.find("#error_alert");

        this.initialiseFormWithData();
    },
    initialiseFormWithData: function() {
        for(inputGroup of this.inputGroups) {
            inputGroup.enabledOrDisable();
        }

        if(this.hospitalNumber3Textbox.val() !== '') {
            this.visibleHospitalNumbers = 3
        } else if (this.hospitalNumber2Textbox.val() !== '') {
            this.visibleHospitalNumbers = 2
        } else {
            this.visibleHospitalNumbers = 1
        }
        this.makeHospitalNumbersVisible()
    },
    setupSubmitButton: function () {
        // var that = this;
        // this.submitButton.click(function (event) {
        //     event.preventDefault();
        //     if (that.validate()) {
        //         that.form.submit();
        //     } else {
        //         that.setValidationRequired();
        //         that.highlightAllErrors();
        //         that.showFormError();
        //     }
        // });
    },
    makeHospitalNumbersVisible: function () {
        if(this.visibleHospitalNumbers >= 2) {
            this.hospitalNumber1Label.html("Hospital Number 1");
            this.hospitalNumber2.removeClass("medex-hidden")
        }
        if(this.visibleHospitalNumbers === 3) {
            this.hospitalNumber3.removeClass("medex-hidden");
            this.hospitalNumberAddBtn.addClass("medex-hidden");
        }
    },
    setupHospitalNumberAddBtn: function () {
        var that = this;
        this.hospitalNumberAddBtn.click(function(event) {
            event.preventDefault();

            that.visibleHospitalNumbers += 1;
            that.makeHospitalNumbersVisible();
        })
    },
    validate: function () {
        let nhsNumberIsValid = this.inputGroups[0].validateTextInputsCheckboxGroup();
        let todIsValid = this.inputGroups[1].validateTextInputsCheckboxGroup();
        let dodIsValid = this.inputGroups[2].validateTextInputsCheckboxGroup();
        let dobIsValid = this.inputGroups[3].validateTextInputsCheckboxGroup();
        let genderIsValid = this.validateGenderRadioButtons();
        let surnameIsValid = this.validateSurname();
        let givenNameIsValid = this.validateGivenName();
        let podIsValid = this.validatePlaceOfDeath();
        let meIsValid = this.validateMeOffice();

        return nhsNumberIsValid && todIsValid && dobIsValid && podIsValid && meIsValid && dodIsValid && genderIsValid && surnameIsValid && givenNameIsValid
    },
    setupSurnameInput: function () {
        this.surnameInput.change(this.validateAndHighlightSurname.bind(this));
    },
    setupGivenNameInput: function () {
        this.givenNameInput.change(this.validateAndHighlightGivenName.bind(this));
    },
    setupGenderRadioButtons: function () {
        var that = this;

        if (this.genderRadioButtons[2].checked) {
          that.genderDetailArea.show()
        } else {
          that.genderDetailArea.hide()
        }

        this.genderRadioButtons.change(
            function () {
                if (this.value === "Other") {
                    that.genderDetailArea.show()
                } else {
                    that.genderDetailArea.hide()
                }
            }
        )
    },
    setupPlaceOfDeath: function () {
        this.placeOfDeathSelect.change(this.validateAndHighlightPlaceOfDeath.bind(this));
    },
    setupMeOffice: function () {
        this.meOfficeSelect.change(this.validateAndHighlightMeOffice.bind(this));
    },
    validateGenderRadioButtons: function () {
      return this.genderMale[0].checked || this.genderFemale[0].checked || this.genderOther[0].checked
    },
    validateAndHighlightMeOffice: function () {
        if (!this.showValidation || this.validateMeOffice()) {
            this.meOfficeDropdown.removeClass("error")
        } else {
            this.meOfficeDropdown.addClass("error")
        }
    },
    validateAndHighlightPlaceOfDeath: function () {
        if (!this.showValidation || this.validatePlaceOfDeath()) {
            this.placeOfDeathDropdown.removeClass("error")
        } else {
            this.placeOfDeathDropdown.addClass("error")
        }
    },
    validatePlaceOfDeath: function () {
        return this.placeOfDeathSelect.val();
    },
    validateMeOffice: function () {
        return this.meOfficeSelect.val();
    },
    validateAndHighlightGenderRadioButtons: function() {
        if (!this.showValidation || this.validateGenderRadioButtons()) {
            this.genderMale.removeClass("error");
            this.genderFemale.removeClass("error");
            this.genderOther.removeClass("error");
        } else {
            this.genderMale.addClass("error");
            this.genderFemale.addClass("error");
            this.genderOther.addClass("error");
        }
    },
    validateAndHighlightSurname: function () {
        if (!this.showValidation || this.validateSurname()) {
            this.surnameInput.removeClass("error");
            this.surnameInput.attr("placeholder", "");
        } else {
            this.surnameInput.addClass("error");
            this.surnameInput.attr("placeholder", REQUIRED_PLACEHOLDER);
        }
    },
    validateAndHighlightGivenName: function () {
        var that = this;
        if (!this.showValidation || this.validateGivenName()) {
            this.givenNameInput.removeClass("error");
            this.givenNameInput.attr("placeholder", "");
        } else {
            this.givenNameInput.addClass("error");
            this.givenNameInput.attr("placeholder", REQUIRED_PLACEHOLDER);
        }
    },
    validateSurname: function () {
        return this.surnameInput.val() !== ''
    },
    validateGivenName: function () {
        return this.givenNameInput.val() !== ''
    },
    setValidationRequired: function () {
        this.showValidation = true;
        for (inputGroup of this.inputGroups) {
            inputGroup.showValidation = true;
        }
    },
    showFormError: function() {
        this.errorAlert.removeClass("medex-hidden");
        window.scrollTo(0, 0);
    },
    highlightAllErrors: function() {
        this.inputGroups[0].validateAndHighlightTextInputsCheckboxGroup();
        this.inputGroups[1].validateAndHighlightTextInputsCheckboxGroup();
        this.inputGroups[2].validateAndHighlightTextInputsCheckboxGroup();
        this.inputGroups[3].validateAndHighlightTextInputsCheckboxGroup();

        this.validateAndHighlightPlaceOfDeath();
        this.validateAndHighlightMeOffice();
        this.validateAndHighlightGivenName();
        this.validateAndHighlightSurname();
        this.validateAndHighlightGenderRadioButtons();
    }

};

var TextInputsCheckboxGroup = function (textboxes, checkbox) {
    this.textboxes = textboxes;
    this.checkbox = checkbox;
    this.showValidation = false;
    this.setup();
};

TextInputsCheckboxGroup.prototype = {
    setup: function () {
        this.setupCheckboxHandler();
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
                that.validateAndHighlightTextInputsCheckboxGroup(that.textboxes, that.checkbox);
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
        for (textInput of that.textboxes) {
            textInput.on('change keyup paste mouseup', function () {
                that.checkbox.prop("disabled", that.anyTextBoxesHaveContent(that.textboxes));
                that.validateAndHighlightTextInputsCheckboxGroup();
            })
        }
    },
    anyTextBoxesHaveContent: function () {
        for (textInput of this.textboxes) {
            if (textInput.val() !== '') {
                return true
            }
        }
        return false
    },
    validateAndHighlightTextInputsCheckboxGroup: function () {

        if (!this.showValidation || this.validateTextInputsCheckboxGroup()) {
            for (textInput of this.textboxes) {
                textInput.removeClass("error")
            }
            this.checkbox.removeClass("error")
        } else {
            for (textInput of this.textboxes) {
                textInput.addClass("error")
            }
            this.checkbox.addClass("error")
        }
    },
    validateTextInputsCheckboxGroup: function () {
        return this.allTextBoxesHaveContent() || this.checkbox.prop('checked')
    },
    allTextBoxesHaveContent: function () {
        for (textInput of this.textboxes) {
            if (textInput.val() === '') {
                return false
            }
        }
        return true
    }
};

$(function () // execute once the DOM has loaded
{
    new Form($(".primary-info-form"));
});
