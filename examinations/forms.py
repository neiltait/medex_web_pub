
class CreateExaminationForm():

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
