from medexCms.utils import parse_datetime


class PatientHeader:
    date_format = '%d.%m.%Y'

    def __init__(self, obj_dict):
        self.given_names = ''
        self.surname = ''
        self.urgency_score = 0
        self.nhs_number = ''
        self.id = ''
        self.time_of_death = ''
        self.date_of_birth = ''
        self.date_of_death = ''
        self.appointment_date = ''
        self.appointment_time = ''
        self.last_admission = ''
        self.case_created_date = ''
        self.admission_notes_added = ''
        self.ready_for_me_scrutiny = ''
        self.unassigned = ''
        self.have_been_scrutinised = ''
        self.pending_admission_notes = ''
        self.pending_discussion_with_qap = ''
        self.pending_discussion_with_representative = ''
        self.pending_scrutiny_notes = ''
        self.have_final_case_outstanding_outcomes = ''
        self.is_cremation = False
        self.is_void = False

        if obj_dict:
            self.fill_from_api(obj_dict)

    def fill_from_api(self, obj_dict):
        self.urgency_score = obj_dict.get("urgencyScore")
        self.given_names = obj_dict.get("givenNames")
        self.surname = obj_dict.get("surname")
        self.nhs_number = obj_dict.get("nhsNumber")
        self.id = obj_dict.get("examinationId")
        self.time_of_death = obj_dict.get("timeOfDeath")
        self.date_of_birth = parse_datetime(obj_dict.get("dateOfBirth"))
        self.date_of_death = parse_datetime(obj_dict.get("dateOfDeath"))
        self.appointment_date = parse_datetime(obj_dict.get("appointmentDate"))
        self.appointment_time = obj_dict.get("appointmentTime")
        self.last_admission = parse_datetime(obj_dict.get("lastAdmission"))
        self.case_created_date = parse_datetime(obj_dict.get("caseCreatedDate"))
        self.admission_notes_added = obj_dict.get("admissionNotesHaveBeenAdded")
        self.ready_for_me_scrutiny = obj_dict.get("readyForMEScrutiny")
        self.unassigned = obj_dict.get("unassigned")
        self.have_been_scrutinised = obj_dict.get("haveBeenScrutinisedByME")
        self.pending_admission_notes = obj_dict.get("pendingAdmissionNotes")
        self.pending_discussion_with_qap = obj_dict.get("pendingDiscussionWithQAP")
        self.pending_discussion_with_representative = obj_dict.get("pendingDiscussionWithRepresentative")
        self.pending_scrutiny_notes = obj_dict.get("pendingScrutinyNotes")
        self.have_final_case_outstanding_outcomes = obj_dict.get("haveFinalCaseOutstandingOutcomes")
        self.is_cremation = obj_dict.get("isCremation", False)
        self.is_void = obj_dict.get("IsVoid", False)

    @property
    def full_name(self):
        return "%s %s" % (self.given_names, self.surname)
