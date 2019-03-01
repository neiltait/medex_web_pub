var showValidation = false;
let REQUIRED_PLACEHOLDER = "Required";

function setSubmitButtonHandler() {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        if (validate()) {
            $("#examination__create--form").submit();
        } else {
            showValidation = true;
            highlightAllErrors();
        }
    });
}

function setGenderDetailsToggle() {
    let moreGenderDetail = $("#more-gender");
    moreGenderDetail.hide();
    $('input[type=radio][name=gender]').change(
        function () {
            if (this.value === "other") {
                moreGenderDetail.show()
            } else {
                moreGenderDetail.hide()
            }
        }
    )
}

function setOnChangeHandlerForNameInputs() {
    $('#last_name').change(validateAndHighlightNames);
    $('#first_name').change(validateAndHighlightNames);
}

function setOnChangeHandlerForPlaceOfDeath() {
    $('#place_of_death').change(validateAndHighlightPlaceOfDeath);
}


function setOnChangeHandlerForMEOffice() {
    $('#me_office').change(validateAndHighlightMEOffice);
}


function setOnChangeHandlerForTextInputsCheckboxGroup(textInputs, checkbox) {
    // add handler for the checkbox
    checkbox.change(
        function () {
            $.each(textInputs, function (index, textInput) {
                if (checkbox.prop('checked')) {
                    textInput[0].disabled = true
                } else {
                    textInput[0].disabled = false
                }
            });
            validateAndHighlightTextInputsCheckboxGroup(textInputs, checkbox);
        }
    );

    // add handler for all textboxes
    for (textInput of textInputs) {
        textInput.on('change keyup paste mouseup', function () {
            checkbox.prop("disabled", anyTextBoxesHaveContent(textInputs));
            validateAndHighlightTextInputsCheckboxGroup(textInputs, checkbox);
        })
    }
}

function allTextBoxesHaveContent(textInputs) {
    for (textInput of textInputs) {
        if (textInput.val() === '') {
            return false
        }
    }
    return true
}

function anyTextBoxesHaveContent(textInputs) {
    for (textInput of textInputs) {
        if (textInput.val() !== '') {
            return true
        }
    }
    return false
}

function validate() {
    let nhsNumberIsValid = validateTextInputsCheckboxGroup([$("#nhs_number")], $("#nhs_number_not_known"));
    let todIsValid = validateTextInputsCheckboxGroup([$("#time_of_death")], $("#time_of_death_not_known"));
    let dodIsValid = validateTextInputsCheckboxGroup([$("#day_of_death"), $("#month_of_death"), $("#year_of_death")], $("#date_of_death_not_known"));
    let dobIsValid = validateTextInputsCheckboxGroup([$("#day_of_birth"), $("#month_of_birth"), $("#year_of_birth")], $("#date_of_birth_not_known"));
    let genderIsValid = validateGenderRadioButtons();
    let nameIsValid = validateName();
    let podIsValid = validatePlaceOfDeath();
    let meIsValid = validateMEOffice();

    return nhsNumberIsValid && todIsValid && dobIsValid && podIsValid && meIsValid && dodIsValid && genderIsValid && nameIsValid
}

function validateTextInputsCheckboxGroup(textInputs, checkbox) {
    return allTextBoxesHaveContent(textInputs) || checkbox.prop('checked')
}

function validateGenderRadioButtons() {
    return $("#gender-1")[0].checked || $("#gender-2")[0].checked || $("#gender-3")[0].checked
}

function validateName() {
    return $('#last_name').val() !== '' && $('#first_name').val() !== ''
}

function validatePlaceOfDeath() {
    return $('#place_of_death').val()
}

function validateMEOffice() {
    return $('#me_office').val()
}

function highlightAllErrors() {
    validateAndHighlightTextInputsCheckboxGroup([$("#nhs_number")], $("#nhs_number_not_known"));
    validateAndHighlightTextInputsCheckboxGroup([$("#time_of_death")], $("#time_of_death_not_known"));
    validateAndHighlightTextInputsCheckboxGroup([$("#day_of_death"), $("#month_of_death"), $("#year_of_death")], $("#date_of_death_not_known"));
    validateAndHighlightTextInputsCheckboxGroup([$("#day_of_birth"), $("#month_of_birth"), $("#year_of_birth")], $("#date_of_birth_not_known"));
    validateAndHighlightGenderRadioButtons();
    validateAndHighlightPlaceOfDeath();
    validateAndHighlightMEOffice();
    validateAndHighlightNames();
}

function validateAndHighlightTextInputsCheckboxGroup(textInputs, checkbox) {
    if (!showValidation || validateTextInputsCheckboxGroup(textInputs, checkbox)) {
        for (textInput of textInputs) {
            textInput.removeClass("error")
        }
        checkbox.removeClass("error")
    } else {
        for (textInput of textInputs) {
            textInput.addClass("error")
        }
        checkbox.addClass("error")
    }
}

function validateAndHighlightGenderRadioButtons() {
    if (!showValidation || validateGenderRadioButtons()) {
        $("#gender-1").removeClass("error");
        $("#gender-2").removeClass("error");
        $("#gender-3").removeClass("error");
    } else {
        $("#gender-1").addClass("error");
        $("#gender-2").addClass("error");
        $("#gender-3").addClass("error");
    }
}

function validateAndHighlightPlaceOfDeath() {
    if (!showValidation || validatePlaceOfDeath()) {
        $('#place_of_death_dropdown').removeClass("error")
    } else {
        $('#place_of_death_dropdown').addClass("error")
    }
}

function validateAndHighlightMEOffice() {
    if (!showValidation || validateMEOffice()) {
        $('#me_office_dropdown').removeClass("error")
    } else {
        $('#me_office_dropdown').addClass("error")
    }
}

function validateAndHighlightNames() {
    if (!showValidation || validateName()) {
        $('#last_name').removeClass("error");
        $('#last_name').attr("placeholder", "");
        $('#first_name').removeClass("error");
        $('#first_name').attr("placeholder", "");
    } else {
        $('#last_name').addClass("error");
        $('#last_name').attr("placeholder", REQUIRED_PLACEHOLDER);
        $('#first_name').addClass("error");
        $('#first_name').attr("placeholder", REQUIRED_PLACEHOLDER);
    }
}


$(function () // execute once the DOM has loaded
{
    setSubmitButtonHandler();
    setOnChangeHandlerForNameInputs();
    setGenderDetailsToggle();
    setOnChangeHandlerForTextInputsCheckboxGroup([$("#nhs_number")], $("#nhs_number_not_known"));
    setOnChangeHandlerForTextInputsCheckboxGroup([$("#time_of_death")], $("#time_of_death_not_known"));
    setOnChangeHandlerForTextInputsCheckboxGroup([$("#day_of_death"), $("#month_of_death"), $("#year_of_death")], $("#date_of_death_not_known"));
    setOnChangeHandlerForTextInputsCheckboxGroup([$("#day_of_birth"), $("#month_of_birth"), $("#year_of_birth")], $("#date_of_birth_not_known"));
    setOnChangeHandlerForPlaceOfDeath();
    setOnChangeHandlerForMEOffice();
});
