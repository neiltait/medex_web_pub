from medexCms.utils import is_empty_date, parse_datetime


class BereavedRepresentative:

    def __init__(self, obj_dict={}):
        self.full_name = obj_dict.get("fullName")
        self.relationship = obj_dict.get("relationship")
        self.phone_number = obj_dict.get("phoneNumber")
        self.present_at_death = obj_dict.get("presentAtDeath")
        self.informed = obj_dict.get("informed")
        self.appointment_time = obj_dict.get("appointmentTime")

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

    def equals(self, representative):
        return representative is not None and \
               self.full_name == representative.full_name and \
               self.relationship == representative.relationship and \
               self.phone_number == representative.phone_number


class DropdownPerson:

    def __init__(self, obj_dict):
        self.person_id = obj_dict.get('userId')
        self.name = obj_dict.get('firstName') + ' ' + obj_dict.get('lastName')
