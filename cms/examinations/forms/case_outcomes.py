class OutstandingItemsForm:

    def __init__(self, form_data):
        self.mccd_issued = form_data.get('mccd_issued')
        self.cremation_form = form_data.get('cremation_form')
        self.gp_notified = form_data.get('gp_notified')

    def for_request(self):
        return {
            "mccdIssued": True if self.mccd_issued == 'true' else False,
            "cremationFormStatus": self.cremation_form,
            "gpNotifiedStatus": self.gp_notified
        }
