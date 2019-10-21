from django import template

from examinations import constants

register = template.Library()


@register.filter()
def case_card_presenter(case):
    """

    :param case: ExaminationOverview
    :return: dict
    """

    def display_date(date, format='%d.%m.%Y', fallback=None):
        return date.strftime(format) if date else fallback

    def display_time(time_string, fallback=None):
        return time_string if time_string and time_string != '00:00:00' else fallback

    def display_age(case, fallback=None):
        calculated_age = case.calc_age()
        return calculated_age if calculated_age else fallback

    def display(value, fallback=None):
        return value if value else fallback

    return {
        'id': case.id,
        'full_name': "%s %s" % (case.given_names, case.surname),
        'banner_dob': display_date(case.date_of_birth, fallback='Unknown'),
        'banner_dod': display_date(case.date_of_death, fallback='Unknown'),
        'card_dob': display_date(case.date_of_birth, fallback='Unknown'),
        'card_dod': display_date(case.date_of_death, fallback='Unknown'),
        'card_tod': display_time(case.time_of_death, fallback='Unknown'),
        'age': display_age(case, fallback='-'),
        'has_last_admission': True if case.last_admission else False,
        'last_admission_days_ago': case.calc_last_admission_days_ago(),
        'created_days_ago': case.calc_created_days_ago(),
        'urgent': case.urgent(),
        'nhs_number': display(case.nhs_number, fallback='Unknown'),
        'appointment_date': display_date(case.appointment_date, fallback='-'),
        'case_created_date': display_date(case.case_created_date, fallback='Unknown'),
        'case_closed_date': display_date(case.case_closed_date, fallback='-'),
        'case_outcome': constants.get_display_outcome_summary(case.case_outcome),
        'appointment_time': case.appointment_time if
        case.appointment_time and case.appointment_time != '00:00:00' else '-'
    }
