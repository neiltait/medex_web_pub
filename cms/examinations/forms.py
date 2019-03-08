
class PrimaryExaminationInformationForm():

  def __init__(self, request=None):
    if request:
      self.last_name = request.get('last_name')
      self.first_name = request.get('first_name')
      self.gender = request.get('gender')
      self.nhs_number = request.get('nhs_number')
      self.nhs_number_not_known = request.get('nhs_number_not_known')
      self.hospital_number = request.get('hospital_number')
      self.date_of_birth = request.get('date_of_birth')
      self.date_of_death = request.get('date_of_death')
      self.time_of_death = request.get('time_of_death')
      self.place_of_death = request.get('place_of_death')
    else:
      self.first_name = ''
      self.last_name =  ''
      self.gender = ''
      self.nhs_number = ''
      self.nhs_number_not_known = ''
      self.hospital_number = ''
      self.date_of_birth = ''
      self.date_of_death = ''
      self.time_of_death = ''
      self.place_of_death = ''


class SecondaryExaminationInformationForm:

  def __init__(self, request=None):
    if request:
      self.address_line_1 = request.get('address_line_1')
      self.address_line_2 = request.get('address_line_2')
      self.address_town = request.get('address_town')
      self.address_county = request.get('address_county')
      self.address_postcode = request.get('address_postcode')
      self.relevant_occupation = request.get('relevant_occupation')
      self.care_organisation = request.get('care_organisation')
      self.funeral_arrangements = request.get('funeral_arrangements')
      self.implanted_devices = request.get('implanted_devices')
      self.implanted_devices_details = request.get('implanted_devices_details')
      self.funeral_directors = request.get('funeral_directors')
      self.personal_effects = request.get('personal_effects')
      self.personal_effects_details = request.get('personal_effects_details')
    else:
      self.address_line_1 = ''
      self.address_line_2 = ''
      self.address_town = ''
      self.address_county = ''
      self.address_postcode = ''
      self.relevant_occupation = ''
      self.care_organisation = ''
      self.funeral_arrangements = ''
      self.implanted_devices = ''
      self.funeral_directors = ''
      self.personal_effects = ''


class BereavedInformationForm:

  def __init__(self, request=None):
    if request:
      self.bereaved_name = request.get('bereaved_name')
      self.relationship = request.get('relationship')
      self.present_death = request.get('present_death')
      self.phone_number = request.get('phone_number')
      self.informed = request.get('informed')
      self.day_of_appointment = request.get('day_of_appointment')
      self.month_of_appointment = request.get('month_of_appointment')
      self.year_of_appointment = request.get('year_of_appointment')
      self.time_of_appointment = request.get('time_of_appointment')
      self.appointment_additional_details = request.get('appointment_additional_details')
    else:
      self.bereaved_name = ''
      self.relationship = ''
      self.present_death = ''
      self.phone_number = ''
      self.informed = ''
      self.day_of_appointment = ''
      self.month_of_appointment = ''
      self.year_of_appointment = ''
      self.time_of_appointment = ''
      self.appointment_additional_details = ''


class UrgencyInformationForm:

  def __init__(self, request=None):
    if request:
      self.faith_death = request.get('faith_death')
      self.coroner_case = request.get('coroner_case')
      self.child_death = request.get('child_death')
      self.cultural_death = request.get('cultural_death')
      self.other = request.get('other')
      self.urgency_additional_details = request.get('urgency_additional_details')
    else:
      self.faith_death = ''
      self.coroner_case = ''
      self.child_death = ''
      self.cultural_death = ''
      self.other = ''
      self.urgency_additional_details = ''
