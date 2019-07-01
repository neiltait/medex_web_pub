from medexCms.utils import is_empty_date, parse_datetime, fallback_to
from people import request_handler


class BereavedRepresentative:

    def __init__(self, obj_dict={}):
        self.full_name = fallback_to(obj_dict.get("fullName"), '')
        self.relationship = fallback_to(obj_dict.get("relationship"), '')
        self.phone_number = fallback_to(obj_dict.get("phoneNumber"), '')
        self.present_at_death = obj_dict.get("presentAtDeath") if obj_dict.get("presentAtDeath") else None
        self.informed = obj_dict.get("informed") if obj_dict.get("informed") else None
        self.appointment_time = obj_dict.get("appointmentTime")
        self.appointment_notes = fallback_to(obj_dict.get("notes"), '')

        if not is_empty_date(obj_dict.get("appointmentDate")) and obj_dict.get("appointmentDate") is not None:
            self.appointment_date = parse_datetime(obj_dict.get("appointmentDate"))
            self.appointment_day = self.appointment_date.day
            self.appointment_month = self.appointment_date.month
            self.appointment_year = self.appointment_date.year
        else:
            self.appointment_date = None
            self.appointment_day = None
            self.appointment_month = None
            self.appointment_year = None

    def set_values_from_form(self, obj_dict):
        self.full_name = obj_dict.get('bereaved_name')
        self.relationship = obj_dict.get('relationship')
        self.phone_number = obj_dict.get('phone_number')
        self.present_at_death = obj_dict.get('present_death')
        self.informed = obj_dict.get('informed')
        self.appointment_time = obj_dict.get("time_of_appointment")
        self.appointment_day = obj_dict.get('day_of_appointment')
        self.appointment_month = obj_dict.get('month_of_appointment')
        self.appointment_year = obj_dict.get('year_of_appointment')
        self.appointment_notes = obj_dict.get('appointment_notes')

    def equals(self, representative):
        return representative is not None and \
               self.full_name == representative.full_name and \
               self.relationship == representative.relationship and \
               self.phone_number == representative.phone_number


class DropdownPerson:

    def __init__(self, obj_dict):
        self.person_id = obj_dict.get('userId')
        if 'fullName' in obj_dict:
            self.name = obj_dict.get('fullName')
        else:
            self.name = obj_dict.get('firstName') + ' ' + obj_dict.get('lastName')

    @classmethod
    def get_medical_examiners(cls, auth_token, examination_id):
        return request_handler.get_medical_examiners_list_for_examination(auth_token, examination_id)

    @classmethod
    def get_meos(cls, auth_token, examination_id):
        return request_handler.get_medical_examiners_officers_list_for_examination(auth_token, examination_id)
