from medexCms.api import enums


class OutstandingItemsForm:

    def __init__(self, form_data):
        self.mccd_issued = form_data.get('mccd_issued')
        self.cremation_form = form_data.get('cremation_form')
        self.gp_notified = form_data.get('gp_notified')
        self.waive_fee = self.parse_waive_fee(form_data)

    @staticmethod
    def parse_waive_fee(form_data: dict) -> None or bool:
        """
        Return None if no cremation form, otherwise return bool from waive_fee.
        """
        if form_data.get('cremation_form') != enums.yes_no.YES:
            return None
        return form_data.get('waive_fee', False)

    def for_request(self):
        return {
            "mccdIssued": True if self.mccd_issued == 'true' else False,
            "cremationFormStatus": self.cremation_form,
            "gpNotifiedStatus": self.gp_notified,
            "waiveFee": self.waive_fee
        }
