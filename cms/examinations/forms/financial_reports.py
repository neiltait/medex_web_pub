from alerts.messages import ErrorFieldRequiredMessage, INVALID_DATE
from medexCms.utils import build_date, validate_date, API_DATE_FORMAT


class FinancialReportsForm:

    def __init__(self, request=None):
        self.initialise_errors()
        if request:
            self.initialise_form_from_data(request)
        else:
            self.initialise_blank_form()

    def initialise_blank_form(self):
        self.me_office = ""
        self.day_from = ""
        self.month_from = ""
        self.year_from = ""
        self.day_to = ""
        self.month_to = ""
        self.year_to = ""

    def initialise_form_from_data(self, request):
        self.me_office = request.get("me_office")

        self.day_from = request.get("day_from")
        self.month_from = request.get("month_from")
        self.year_from = request.get("year_from")

        self.day_to = request.get("day_to")
        self.month_to = request.get("month_to")
        self.year_to = request.get("year_to")

    def filter_to_not_blank_values(self, a_list):
        not_empty = []
        for item in a_list:
            if item != '':
                not_empty.append(item)
        return not_empty

    def initialise_errors(self):
        self.errors = {"count": 0}

    @property
    def error_count(self):
        return self.errors['count']

    def is_valid(self):
        self.errors["count"] = 0

        if self.me_office is None or len(self.me_office.strip()) == 0:
            self.errors["me_office"] = ErrorFieldRequiredMessage("a location")
            self.errors["count"] += 1

        if not self.text_group_contains_valid_date(self.day_from, self.month_from,
                                                   self.year_from):
            self.errors["date_from"] = INVALID_DATE
            self.errors["count"] += 1

        if not self.text_group_contains_valid_date(self.day_to, self.month_to,
                                                   self.year_to):
            self.errors["date_to"] = INVALID_DATE
            self.errors["count"] += 1

        return self.errors["count"] == 0

    def to_object(self):
        date_from = build_date(self.year_from, self.month_from, self.day_from).strftime(API_DATE_FORMAT)
        date_to = build_date(self.year_to, self.month_to, self.day_to).strftime(API_DATE_FORMAT)

        return {
            "me_office": self.me_office,
            "date_from": date_from,
            "date_to": date_to,
        }

    def text_group_contains_valid_date(self, day, month, year):
        return validate_date(year, month, day)
