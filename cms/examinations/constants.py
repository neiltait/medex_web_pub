def get_display_short_user_role(role, default=''):
    short_user_roles = {
        'MedicalExaminerOfficer': 'MEO',
        'MedicalExaminer': 'ME',
        'MEO': 'MEO',
        'ME': 'ME',
    }
    return __get_dictionary_value(role, short_user_roles, default)


def get_display_bereaved_outcome(outcome):
    outcomes = {
        'ConcernsCoronerInvestigation': 'Coroner investigation',
        'ConcernsRequires100a': 'Requires 100a',
        'ConcernsAddressedWithoutCoroner': 'Concerns were addressed without the coroner',
        'CauseOfDeathAccepted': 'Cause of death accepted'
    }
    return __get_dictionary_value(outcome, outcomes)


def get_display_qap_outcome(outcome):
    outcomes = {
        'MccdCauseOfDeathProvidedByQAP': 'Issue MCCD. New cause of death from QAP',
        'MccdCauseOfDeathProvidedByME': 'Issue MCCD. Original cause of death from ME',
        'MccdCauseOfDeathAgreedByQAPandME': 'Issue MCCD. New cause of death agreed between QAP and ME',
        'ReferToCoroner': 'Refer case to coroner'
    }
    return __get_dictionary_value(outcome, outcomes)


def __get_dictionary_value(key, dictionary, default=''):
    if key in dictionary:
        return dictionary[key]
    else:
        return default
