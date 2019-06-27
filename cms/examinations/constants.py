def get_display_short_user_role(role, default=''):
    short_user_roles = {
        'MedicalExaminerOfficer': 'MEO',
        'MedicalExaminer': 'ME',
        'MEO': 'MEO',
        'ME': 'ME',
        'ServiceOwner': 'SO',
        'ServiceAdministrator': 'SA'
    }
    return __get_dictionary_value(role, short_user_roles, default)

def get_display_user_role(role, default=''):
    user_roles = {
        'MedicalExaminerOfficer': 'Medical Examiner Officer',
        'MedicalExaminer': ' Medical Examiner',
        'ServiceOwner': 'Service Owner',
        'ServiceAdministrator': 'Service Administrator'
    }
    return __get_dictionary_value(role, user_roles, default)



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
        'ReferToCoronerFor100a': '',
        'ReferToCoronerInvestigation': ''
    }
    return __get_dictionary_value(outcome, outcomes)


def get_display_qap_high_outcome(outcome):
    outcomes = {
        'MccdCauseOfDeathProvidedByQAP': 'Issue MCCD',
        'MccdCauseOfDeathProvidedByME': 'Issue MCCD',
        'MccdCauseOfDeathAgreedByQAPandME': 'Issue MCCD',
        'ReferToCoronerFor100a': 'Refer case to coroner for permission to issue an MCCD with 100a',
        'ReferToCoronerInvestigation': 'Refer case for coroner investigation'
    }
    return __get_dictionary_value(outcome, outcomes)


def get_display_circumstances_of_death(circumstance):
    circumstances_of_death = {
        'Expected': 'Expected',
        'Unexpected': 'Unexpected',
        'SuddenButNotUnexpected': 'Sudden but not unexpected',
        'PartOfAnIndividualisedEndOfLifeCarePlan': 'Part of an individualised end of life care plan'
    }
    return __get_dictionary_value(circumstance, circumstances_of_death)


def get_display_scrutiny_outcome(outcome):
    outcomes = {
        'IssueAnMccd': 'Issue an MCCD',
        'ReferToCoronerFor100a': 'Refer case to coroner for permission to issue an MCCD with 100a',
        'ReferToCoronerInvestigation': 'Refer case to coroner for an investigation'
    }
    return __get_dictionary_value(outcome, outcomes)


def get_display_outcome_summary(outcome):
    outcomes = {
        'IssueMCCD': 'Issue an MCCD',
        'IssueMCCDWith100a': 'Issue an MCCD with 100a',
        'ReferToCoroner': 'Refer case to coroner'
    }
    return __get_dictionary_value(outcome, outcomes)


def __get_dictionary_value(key, dictionary, default=''):
    if key in dictionary:
        return dictionary[key]
    else:
        return default
