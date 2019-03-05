from alerts.messages import ErrorFieldRequiredMessage


class PrimaryExaminationInformationForm:

    def __init__(self, request=None):
        self.initialiseErrors()
        if request:
            self.initialise_form_from_data(request)
        else:
            self.initialise_blank_form()

    def initialise_blank_form(self):
        self.first_name = ""
        self.last_name = ""
        self.gender = ""
        self.gender_details = ""
        self.nhs_number = ""
        self.nhs_number_not_known = ""
        self.hospital_number_1 = ""
        self.hospital_number_2 = ""
        self.hospital_number_3 = ""
        self.date_of_birth = ""
        self.date_of_birth_not_known = ""
        self.date_of_death = ""
        self.date_of_death_not_known = ""
        self.time_of_death = ""
        self.time_of_death_not_known = ""
        self.place_of_death = ""

    def initialise_form_from_data(self, request):
        self.last_name = request.get("last_name")
        self.first_name = request.get("first_name")
        self.gender = request.get("gender")
        self.gender_details = request.get("gender_details")
        self.nhs_number = request.get("nhs_number")
        self.nhs_number_not_known = request.get("nhs_number_not_known")
        self.hospital_number_1 = request.get("hospital_number_1")
        self.hospital_number_2 = request.get("hospital_number_2")
        self.hospital_number_3 = request.get("hospital_number_3")
        self.day_of_birth = request.get("day_of_birth")
        self.month_of_birth = request.get("month_of_birth")
        self.year_of_birth = request.get("year_of_birth")
        self.date_of_birth_not_known = request.get("date_of_birth_not_known")
        self.day_of_death = request.get("day_of_death")
        self.month_of_death = request.get("month_of_death")
        self.year_of_death = request.get("year_of_death")
        self.date_of_death_not_known = request.get("date_of_death_not_known")
        self.time_of_death = request.get("time_of_death")
        self.time_of_death_not_known = request.get("time_of_death_not_known")
        self.place_of_death = request.get("place_of_death")
        self.me_office = request.get("me_office")
        self.out_of_hours = request.get("out_of_hours")

    def initialiseErrors(self):
        self.first_name_error = None
        self.last_name_error = None
        self.nhs_number_error = None
        self.gender_error = None
        self.date_of_death_error = None
        self.time_of_death_error = None
        self.date_of_birth_error = None
        self.place_of_death_error = None
        self.me_office_error = None

    def is_valid(self):
        self.has_errors = False

        if self.first_name is None:
            self.first_name_error = ErrorFieldRequiredMessage('first name')
            self.has_errors = True

        if self.last_name is None:
            self.last_name_error = ErrorFieldRequiredMessage('last name')
            self.has_errors = True

        if self.gender is None:
            self.gender_error = ErrorFieldRequiredMessage('gender')
            self.has_errors = True

        if not self.text_and_checkbox_group_is_valid([self.nhs_number], self.nhs_number_not_known):
            self.nhs_number_error = ErrorFieldRequiredMessage('NHS number')
            self.has_errors = True

        if not self.text_and_checkbox_group_is_valid([self.time_of_death], self.time_of_death_not_known):
            self.time_of_death_error = ErrorFieldRequiredMessage('time of death')
            self.has_errors = True

        if not self.text_and_checkbox_group_is_valid([self.day_of_birth, self.month_of_birth, self.year_of_birth], self.date_of_birth_not_known):
            self.date_of_birth_error = ErrorFieldRequiredMessage('date of birth')
            self.has_errors = True

        if not self.text_and_checkbox_group_is_valid([self.day_of_death, self.month_of_death, self.year_of_death], self.date_of_death_not_known):
            self.date_of_death_error = ErrorFieldRequiredMessage('date of death')
            self.has_errors = True

        if self.place_of_death is None:
            self.place_of_death_error = ErrorFieldRequiredMessage("place of death")
            self.has_errors = True

        if self.me_office is None:
            self.me_office_error = ErrorFieldRequiredMessage("ME office")
            self.has_errors = True

        return not self.has_errors

    def text_and_checkbox_group_is_valid(self, textboxes, checkbox):
        if checkbox is None or checkbox is False:
            for textbox in textboxes:
                if textbox is None or len(textbox.strip()) == 0:
                    return False
        return True

