class IndexOverview:

    def __init__(self, location, response):
        self.view_location = location if location else 'All permitted'
        self.total_cases = response.get('countOfTotalCases')
        self.urgent_cases = response.get('countOfUrgentCases')
        self.count_admission_notes_added = response.get('countOfCasesAdmissionNotesHaveBeenAdded')
        self.count_scrutiny_ready = response.get('countOfCasesReadyForMEScrutiny')
        self.count_unassigned = response.get('countOfCasesUnassigned')
        self.count_scrutiny_complete = response.get('countOfCasesHaveBeenScrutinisedByME')
        self.count_admission_notes_pending = response.get('countOfCasesPendingAdmissionNotes')
        self.count_qap_discussion_pending = response.get('countOfCasesPendingDiscussionWithQAP')
        self.count_representative_discussion_pending = response.get('countOfCasesPendingDiscussionWithRepresentative')
        self.count_final_outcome_outstanding = response.get('countOfCasesHaveFinalCaseOutstandingOutcomes')
