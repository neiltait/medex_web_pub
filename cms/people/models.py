from medexCms.utils import is_empty_date, parse_datetime


class BereavedRepresentative:

    def __init__(self, obj_dict):
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


class DropdownPerson:

    def __init__(self, obj_dict):
        self.person_id = obj_dict.get('userId')
        self.name = obj_dict.get('firstName') + ' ' + obj_dict.get('lastName')
