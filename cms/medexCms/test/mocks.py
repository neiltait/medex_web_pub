import json

from datetime import datetime

from requests.models import Response
from rest_framework import status

from medexCms import settings
from medexCms.utils import NONE_DATE, API_DATE_FORMAT


class SessionMocks:
    ACCESS_TOKEN = "c15be3d1-513f-49dc-94f9-47449c1cfeb8"
    ID_TOKEN_NAME = "8a89be6d-70df-4b21-9d6e-82873d7ff1b0"

    @classmethod
    def get_auth_cookies(cls):
        return {
            settings.AUTH_TOKEN_NAME: cls.ACCESS_TOKEN,
            settings.ID_TOKEN_NAME: cls.ID_TOKEN_NAME
        }

    @classmethod
    def get_auth_token(cls):
        return {
            "access_token": cls.ACCESS_TOKEN,
            "id_token": cls.ID_TOKEN_NAME,
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "openid profile email",
        }

    @classmethod
    def get_validate_response_user_dict(cls):
        return {
            'userId': '1',
            'firstName': 'Test',
            'lastName': 'User',
            'emailAddress': 'test.user@email.com',
        }

    @classmethod
    def get_successful_token_generation_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_auth_token()).encode('utf-8')
        return response

    @classmethod
    def get_successful_validate_session_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_validate_response_user_dict()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_validate_session_response(cls):
        response = Response()
        response.status_code = status.HTTP_401_UNAUTHORIZED
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_logout_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        return response


class UserMocks:
    USER_ID = 1

    @classmethod
    def get_empty_user_dict(cls):
        return {
            'userId': None,
            'firstName': None,
            'lastName': None,
            'email': None,
        }

    @classmethod
    def get_filled_user_dict(cls):
        return {
            'userId': '1',
            'firstName': 'Test',
            'lastName': 'User',
            'email': 'test.user@email.com',
        }

    @classmethod
    def get_me_user_list(cls):
        return [
            {
                "userId": "1",
                "firstName": "Dr Susan",
                "lastName": "Chang",
                "email": "s.chang@nhs.uk",
                "userRole": "MedicalExaminer"
            },
            {
                "userId": "2",
                "firstName": "Dr Andrew",
                "lastName": "McCloud",
                "email": "a.mccloud@nhs.uk",
                "userRole": "MedicalExaminer"
            },
            {
                "userId": "3",
                "firstName": "Dr Anders",
                "lastName": "Petersen",
                "email": "a.petersen@nhs.uk",
                "userRole": "MedicalExaminer"
            },
            {
                "userId": "4",
                "firstName": "Dr Subhashine",
                "lastName": "Sanapala",
                "email": "s.sanapala@nhs.uk",
                "userRole": "MedicalExaminer"
            },
            {
                "userId": "5",
                "firstName": "Dr Ore",
                "lastName": "Thompson",
                "email": "o.thompson@nhs.uk",
                "userRole": "MedicalExaminer"
            }
        ]

    @classmethod
    def get_meo_user_list(cls):
        return [
            {
                'userId': '6',
                'firstName': 'Sofia',
                'lastName': 'Skouros',
                "userRole": "MedicalExaminerOfficer"
            },
            {
                'userId': '7',
                'firstName': 'Alex',
                'lastName': 'McPherson',
                "userRole": "MedicalExaminerOfficer"
            },
            {
                'userId': '8',
                'firstName': 'Suchi',
                'lastName': 'Kandukuri',
                "userRole": "MedicalExaminerOfficer"
            }
        ]

    @classmethod
    def get_medical_examiners_load_response_content(cls):
        return {
            'users': cls.get_me_user_list()
        }

    @classmethod
    def get_successful_user_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({'userId': cls.USER_ID}).encode('utf-8')
        return response

    @classmethod
    def get_successful_single_user_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_filled_user_dict()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_user_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_400_BAD_REQUEST
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_single_user_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(cls.get_empty_user_dict()).encode('utf-8')
        return response


class PermissionMocks:
    PERMISSION_ID = 1
    ME_TYPE = 'me'
    MEO_TYPE = 'meo'

    @classmethod
    def get_meo_permission_dict(cls):
        return {
            "permissionId": "123-456-789",
            "userId": "abc-def-ghi",
            "locationId": "jkl-mno-pqr",
            "userRole": '0',
        }

    @classmethod
    def get_me_permission_dict(cls):
        return {
            "permissionId": "123-456-789",
            "userId": "abc-def-ghi",
            "locationId": "jkl-mno-pqr",
            "userRole": '1',
        }

    @classmethod
    def get_user_permission_response_content(cls, role_type=ME_TYPE):
        permission_dict = cls.get_me_permission_dict() if role_type == cls.ME_TYPE else cls.get_meo_permission_dict()
        return {
            "permissions": [
                permission_dict
            ],
            "errors": {
                "additionalProp1": [
                    "string"
                ],
                "additionalProp2": [
                    "string"
                ],
                "additionalProp3": [
                    "string"
                ]
            },
            "success": True
        }

    @classmethod
    def get_successful_permission_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({'permissionId': cls.PERMISSION_ID}).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_permission_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_400_BAD_REQUEST
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_permission_load_response(cls, role_type=ME_TYPE):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_user_permission_response_content(role_type)).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_permission_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_400_BAD_REQUEST
        response._content = json.dumps(None).encode('utf-8')
        return response


class LocationsMocks:

    @classmethod
    def get_trust_location_list(cls):
        return [
            {
                'id': 1,
                'name': 'Gloucester NHS Trust',
            },
            {
                'id': 2,
                'name': 'Sheffield NHS Trust',
            },
            {
                'id': 3,
                'name': 'Barts NHS Trust',
            }
        ]

    @classmethod
    def get_region_location_list(cls):
        return [
            {
                'id': 1,
                'name': 'North',
            },
            {
                'id': 2,
                'name': 'South',
            },
            {
                'id': 3,
                'name': 'East',
            },
            {
                'id': 4,
                'name': 'West',
            }
        ]

    @classmethod
    def get_me_office_location_list(cls):
        return [
            {
                'id': '1',
                'name': 'Barnet Hospital ME Office',
            },
            {
                'id': '2',
                'name': 'Sheffield Hospital ME Office',
            },
            {
                'id': '3',
                'name': 'Gloucester Hospital ME Office',
            }
        ]


class ExaminationMocks:
    EXAMINATION_ID = 1

    @classmethod
    def get_minimal_create_case_form_data(cls):
        return {
            'last_name': 'Doe',
            'first_name': 'John',
            'gender': 'male',
            'nhs_number_not_known': True,
            'date_of_birth_not_known': True,
            'time_of_death_not_known': True,
            'date_of_death_not_known': True,
            'place_of_death': 1,
            'me_office': 1,
        }

    @classmethod
    def get_patient_details_secondary_info_form_data(cls):
        return {
            'address_line_1': '2 The Street',
            'address_line_2': '',
            'address_town': 'Anyville',
            'address_county': 'London',
            'address_postcode': 'A1 1AA',
            'relevant_occupation': '',
            'care_organisation': 'Anyville Hospital Trust',
            'funeral_arrangements': 'burial',
            'implanted_devices': 'no',
            'implanted_devices_details': '',
            'funeral_directors': 'Anyville Funeral Directors',
            'personal_effects': 'no',
            'personal_effects_details': ''
        }

    @classmethod
    def get_patient_details_bereaved_form_data(cls):
        return {
            'bereaved_name_1': 'Anne Smith',
            'relationship_1': 'Wife',
            'present_death_1': 'no',
            'phone_number_1': '03069 990146',
            'informed_1': 'yes',
            'day_of_appointment_1': '1',
            'month_of_appointment_1': '1',
            'year_of_appointment_1': '2019',
            'time_of_appointment_1': '12:00',
            'bereaved_name_2': 'Bob Smith',
            'relationship_2': 'Son',
            'present_death_2': 'no',
            'phone_number_2': '03069 990146',
            'informed_2': 'yes',
            'day_of_appointment_2': '1',
            'month_of_appointment_2': '1',
            'year_of_appointment_2': '2019',
            'time_of_appointment_2': '12:00',
            'appointment_additional_details': '',
        }

    @classmethod
    def get_patient_details_urgency_form_data(cls):
        return {
            'faith_death': 'yes',
            'coroner_case': 'no',
            'child_death': 'no',
            'cultural_death': 'no',
            'other': 'no',
            'urgency_additional_details': '',
        }

    @classmethod
    def get_medical_team_tab_form_data(cls):
        return {
            'consultant_name_1': 'Dr Deborah Dale',
            'consultant_role_1': 'Cardiologist',
            'consultant_organisation_1': 'Sheffield Hospital',
            'consultant_phone_number_1': '100',
            'consultant_name_2': 'Mr Kiran Sharma',
            'consultant_role_2': 'Transplant surgeon',
            'consultant_organisation_2': 'Sheffield Hospital',
            'consultant_phone_number_2': '200',
            'consultant_name_3': '',
            'consultant_role_3': '',
            'consultant_organisation_3': '',
            'consultant_phone_number_3': '',
            'qap_name': '',
            'qap_role': '',
            'qap_organisation': '',
            'qap_phone_number': '',
            'gp_name': '',
            'gp_role': '',
            'gp_organisation': '',
            'gp_phone_number': '',

        }

    @classmethod
    def get_medical_team_content(cls):
        return {
            'consultantResponsible': {
                'name': 'Dr Arthur Gunz'
            },
            'consultantsOther': [
                {
                    'name': 'Dr Yolanda Anders'
                }
            ],
            'qap': {
                'name': 'Dr Kiran Kandukuri'
            },
            'generalPractitioner': {
                'name': ''
            },
            'medicalExaminer': {
                'userId': '1',
                'firstName': 'Simon',
                'lastName': 'Li',
                'email': 's.li@methods.co.uk'
            },
            'medicalExaminerOfficer': {
                'userId': '2',
                'firstName': 'Janet',
                'lastName': 'Matthews',
                'email': 'j.matthews@methods.co.uk'
            }
        }

    @classmethod
    def get_examination_response_content(cls):
        examination = {
            "id": "1",
            "completed": "False",
            "coronerStatus": "False",
        }
        examination.update(cls.get_minimal_create_case_form_data())
        examination.update(cls.get_patient_details_secondary_info_form_data())
        examination.update(cls.get_patient_details_urgency_form_data())
        examination['representatives'] = [cls.get_patient_details_bereaved_form_data()]

        return examination

    @classmethod
    def get_patient_details_load_response_content(cls):
        return {
            "header": {
                "urgencyScore": 0,
                "givenNames": "John",
                "surname": "Doe",
                "nhsNumber": "123-456-7890",
                "examinationId": "KEK49GWR-GT42GW4-G42GGW4T-WG4G35",
                "timeOfDeath": "10:00",
                "dateOfBirth": "1919-04-15T10:00:01.174Z",
                "dateOfDeath": "2019-04-15T10:00:01.174Z",
                "appointmentDate": "2019-04-15T11:37:01.174Z",
                "appointmentTime": "09:00",
                "lastAdmission": "2019-04-15T11:37:01.174Z",
                "caseCreatedDate": "2019-04-15T11:37:01.174Z",
                "admissionNotesHaveBeenAdded": True,
                "readyForMEScrutiny": True,
                "unassigned": True,
                "haveBeenScrutinisedByME": True,
                "pendingAdmissionNotes": True,
                "pendingDiscussionWithQAP": True,
                "pendingDiscussionWithRepresentative": True,
                "haveFinalCaseOutstandingOutcomes": True
            },
            "id": "0123-456-789",
            "culturalPriority": True,
            "faithPriority": True,
            "childPriority": True,
            "coronerPriority": True,
            "otherPriority": True,
            "priorityDetails": "",
            "completed": True,
            "coronerStatus": "",
            "gender": "Male",
            "genderDetails": "",
            "placeDeathOccured": "",
            "medicalExaminerOfficeResponsible": "",
            "dateOfBirth": "2019-03-22T13:41:07.449Z",
            "dateOfDeath": "2019-03-22T13:41:07.449Z",
            "nhsNumber": "0123-456-789",
            "hospitalNumber_1": "",
            "hospitalNumber_2": "",
            "hospitalNumber_3": "",
            "timeOfDeath": "",
            "givenNames": "John",
            "surname": "Doe",
            "outOfHours": False,
            "postCode": "",
            "houseNameNumber": "",
            "street": "",
            "town": "",
            "county": "",
            "country": "",
            "lastOccupation": "",
            "organisationCareBeforeDeathLocationId": "",
            "modeOfDisposal": "",
            "anyImplants": True,
            "implantDetails": "",
            "funeralDirectors": "",
            "anyPersonalEffects": True,
            "personalEffectDetails": "",
            "representatives": [
            ],
            "errors": {

            },
            "success": True
        }

    @classmethod
    def get_medical_team_load_response_content(cls, examination_id=1):
        if examination_id == 1:
            return {
                "header": {
                    "urgencyScore": 0,
                    "givenNames": "John",
                    "surname": "Doe",
                    "nhsNumber": "123-456-7890",
                    "examinationId": "KEK49GWR-GT42GW4-G42GGW4T-WG4G35",
                    "timeOfDeath": "10:00",
                    "dateOfBirth": "1919-04-15T10:00:01.174Z",
                    "dateOfDeath": "2019-04-15T10:00:01.174Z",
                    "appointmentDate": "2019-04-15T11:37:01.174Z",
                    "appointmentTime": "09:00",
                    "lastAdmission": "2019-04-15T11:37:01.174Z",
                    "caseCreatedDate": "2019-04-15T11:37:01.174Z",
                    "admissionNotesHaveBeenAdded": True,
                    "readyForMEScrutiny": True,
                    "unassigned": True,
                    "haveBeenScrutinisedByME": True,
                    "pendingAdmissionNotes": True,
                    "pendingDiscussionWithQAP": True,
                    "pendingDiscussionWithRepresentative": True,
                    "haveFinalCaseOutstandingOutcomes": True
                },
                "consultantResponsible": {
                    "name": "Peter Hipkiss",
                    "role": "Oncologist",
                    "organisation": "St Thomas's hospital",
                    "phone": "12345",
                    "notes": ""
                },
                "nursingTeamInformation": "",
                "medicalExaminerUserId": "",
                "medicalExaminerOfficerUserId": "",
                "errors": {
                    "additionalProp1": [
                        ""
                    ],
                    "additionalProp2": [
                        ""
                    ],
                    "additionalProp3": [
                        ""
                    ]
                },
                "success": "true"
            }
        elif examination_id == 2:
            return {
                "header": {
                    "urgencyScore": 0,
                    "givenNames": "John",
                    "surname": "Doe",
                    "nhsNumber": "123-456-7890",
                    "examinationId": "KEK49GWR-GT42GW4-G42GGW4T-WG4G35",
                    "timeOfDeath": "10:00",
                    "dateOfBirth": "1919-04-15T10:00:01.174Z",
                    "dateOfDeath": "2019-04-15T10:00:01.174Z",
                    "appointmentDate": "2019-04-15T11:37:01.174Z",
                    "appointmentTime": "09:00",
                    "lastAdmission": "2019-04-15T11:37:01.174Z",
                    "caseCreatedDate": "2019-04-15T11:37:01.174Z",
                    "admissionNotesHaveBeenAdded": True,
                    "readyForMEScrutiny": True,
                    "unassigned": True,
                    "haveBeenScrutinisedByME": True,
                    "pendingAdmissionNotes": True,
                    "pendingDiscussionWithQAP": True,
                    "pendingDiscussionWithRepresentative": True,
                    "haveFinalCaseOutstandingOutcomes": True
                },
                "consultantResponsible": {
                    "name": "Peter Hipkiss",
                    "role": "Oncologist",
                    "organisation": "St Thomas's hospital",
                    "phone": "12345",
                    "notes": ""
                },
                "qap": {
                    "name": "Alessandro da Silva",
                    "role": "General Practitioner",
                    "organisation": "The Heathside Medical Center",
                    "phone": "12345",
                    "notes": ""
                },
                "nursingTeamInformation": "",
                "medicalExaminerUserId": "",
                "medicalExaminerOfficerUserId": "",
                "errors": {
                    "additionalProp1": [
                        ""
                    ],
                    "additionalProp2": [
                        ""
                    ],
                    "additionalProp3": [
                        ""
                    ]
                },
                "success": "true"
            }
        else:
            return {
                "header": {
                    "urgencyScore": 0,
                    "givenNames": "John",
                    "surname": "Doe",
                    "nhsNumber": "123-456-7890",
                    "examinationId": "KEK49GWR-GT42GW4-G42GGW4T-WG4G35",
                    "timeOfDeath": "10:00",
                    "dateOfBirth": "1919-04-15T10:00:01.174Z",
                    "dateOfDeath": "2019-04-15T10:00:01.174Z",
                    "appointmentDate": "2019-04-15T11:37:01.174Z",
                    "appointmentTime": "09:00",
                    "lastAdmission": "2019-04-15T11:37:01.174Z",
                    "caseCreatedDate": "2019-04-15T11:37:01.174Z",
                    "admissionNotesHaveBeenAdded": True,
                    "readyForMEScrutiny": True,
                    "unassigned": True,
                    "haveBeenScrutinisedByME": True,
                    "pendingAdmissionNotes": True,
                    "pendingDiscussionWithQAP": True,
                    "pendingDiscussionWithRepresentative": True,
                    "haveFinalCaseOutstandingOutcomes": True
                },
                "consultantResponsible": {
                    "name": "Peter Hipkiss",
                    "role": "Oncologist",
                    "organisation": "St Thomas's hospital",
                    "phone": "12345",
                    "notes": ""
                },
                "generalPractitioner": {
                    "name": "Patricia van Helden",
                    "role": "General Practitioner",
                    "organisation": "Cotton Street General Surgery",
                    "phone": "12345",
                    "notes": ""
                },
                "qap": {
                    "name": "Alessandro da Silva",
                    "role": "General Practitioner",
                    "organisation": "The Heathside Medical Center",
                    "phone": "12345",
                    "notes": ""
                },
                "nursingTeamInformation": "",
                "medicalExaminerUserId": "4",
                "medicalExaminerOfficerUserId": "2",
                "errors": {
                    "additionalProp1": [
                        ""
                    ],
                    "additionalProp2": [
                        ""
                    ],
                    "additionalProp3": [
                        ""
                    ]
                },
                "success": "true"
            }

    @classmethod
    def get_case_index_response_content(cls):
        return {
            "examinations": [
                {
                    "urgencyScore": 1,
                    "givenNames": "John",
                    "surname": "Doe",
                    "nhsNumber": "123-456-78910",
                    "examinationId": "1",
                    "timeOfDeath": "10:48",
                    "dateOfBirth": "1935-09-18T10:48:15.749Z",
                    "dateOfDeath": "2019-03-18T10:48:15.749Z",
                    "appointmentDate": "2019-03-18T10:48:15.749Z",
                    "appointmentTime": "15:48",
                    "lastAdmission": "2019-03-18T10:48:15.749Z",
                    "caseCreatedDate": "2019-03-18T10:48:15.749Z",
                    "age": "92",
                    "caseCreatedDaysAgo": "4",
                    "lastAdmissionDaysAgo": "3"
                },
                {
                    "urgencyScore": 0,
                    "givenNames": "Jemima",
                    "surname": "Doe",
                    "nhsNumber": "123-456-78910",
                    "examinationId": "2",
                    "timeOfDeath": "11:12",
                    "dateOfBirth": "1937-04-27T10:48:15.749Z",
                    "dateOfDeath": "2019-03-18T10:48:15.749Z",
                    "appointmentDate": "2019-03-18T10:48:15.749Z",
                    "appointmentTime": "15:48",
                    "lastAdmission": "2019-03-18T10:48:15.749Z",
                    "caseCreatedDate": "2019-03-18T10:48:15.749Z",
                    "age": "91",
                    "caseCreatedDaysAgo": "4",
                    "lastAdmissionDaysAgo": "2"
                },
                {
                    "urgencyScore": 0,
                    "givenNames": "Deborah",
                    "surname": "Jones",
                    "nhsNumber": "123-456-78910",
                    "examinationId": "3",
                    "timeOfDeath": "09:45",
                    "dateOfBirth": "1962-05-21T10:48:15.749Z",
                    "dateOfDeath": "2019-03-19T10:48:15.749Z",
                    "appointmentDate": "2019-03-18T10:48:15.749Z",
                    "appointmentTime": "15:48",
                    "lastAdmission": "2019-03-18T10:48:15.749Z",
                    "caseCreatedDate": "2019-03-18T10:48:15.749Z",
                    "age": "91",
                    "caseCreatedDaysAgo": "4",
                    "lastAdmissionDaysAgo": "2"
                }
            ],
            "errors": {
                "additionalProp1": [
                    "string"
                ],
                "additionalProp2": [
                    "string"
                ],
                "additionalProp3": [
                    "string"
                ]
            },
            "success": True
        }

    @classmethod
    def get_pre_scrutiny_create_event_data(cls):
        return {
            'me-thoughts': "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman.",
            'cod': 'Expected',
            'possible-cod-1a': 'Cause of death',
            'possible-cod-1b': '',
            'possible-cod-1c': '',
            'possible-cod-2': '',
            'ops': 'IssueAnMccd',
            'gr': 'Yes',
            'grt': 'Palliative care were called too late.',
            'add-event-to-timeline': 'pre-scrutiny'
        }

    @classmethod
    def get_case_outcome_response_data(cls):
        return {
            "caseHeader": {
                "urgencyScore": 0,
                "givenNames": "John",
                "surname": "Doe",
                "nhsNumber": "123-456-7890",
                "examinationId": "KEK49GWR-GT42GW4-G42GGW4T-WG4G35",
                "timeOfDeath": "10:00",
                "dateOfBirth": "1919-04-15T10:00:01.174Z",
                "dateOfDeath": "2019-04-15T10:00:01.174Z",
                "appointmentDate": "2019-04-15T11:37:01.174Z",
                "appointmentTime": "09:00",
                "lastAdmission": "2019-04-15T11:37:01.174Z",
                "caseCreatedDate": "2019-04-15T11:37:01.174Z",
                "admissionNotesHaveBeenAdded": True,
                "readyForMEScrutiny": True,
                "unassigned": True,
                "haveBeenScrutinisedByME": True,
                "pendingAdmissionNotes": True,
                "pendingDiscussionWithQAP": True,
                "pendingDiscussionWithRepresentative": True,
                "haveFinalCaseOutstandingOutcomes": True
            },
            "caseOutcomeSummary": "ReferToCoroner",
            "outcomeOfRepresentativeDiscussion": "CauseOfDeathAccepted",
            "outcomeOfPrescrutiny": "IssueAnMccd",
            "outcomeQapDiscussion": "MccdCauseOfDeathProvidedByQAP",
            "caseOpen": True,
            "scrutinyConfirmedOn": "2019-04-15T11:37:01.174Z",
            "coronerReferral": True,
            "caseMedicalExaminerFullName": "Dr Bob Smith",
            "mccdIssed": False,
            "cremationFormStatus": "",
            "gpNotifedStatus": ""
        }

    @classmethod
    def get_case_breakdown_response_content(cls):
        return {
            "header": {
                "urgencyScore": 0,
                "givenNames": "John",
                "surname": "Doe",
                "nhsNumber": "123-456-7890",
                "examinationId": "KEK49GWR-GT42GW4-G42GGW4T-WG4G35",
                "timeOfDeath": "10:00",
                "dateOfBirth": "1919-04-15T10:00:01.174Z",
                "dateOfDeath": "2019-04-15T10:00:01.174Z",
                "appointmentDate": "2019-04-15T11:37:01.174Z",
                "appointmentTime": "09:00",
                "lastAdmission": "2019-04-15T11:37:01.174Z",
                "caseCreatedDate": "2019-04-15T11:37:01.174Z",
                "admissionNotesHaveBeenAdded": True,
                "readyForMEScrutiny": True,
                "unassigned": True,
                "haveBeenScrutinisedByME": True,
                "pendingAdmissionNotes": True,
                "pendingDiscussionWithQAP": True,
                "pendingDiscussionWithRepresentative": True,
                "haveFinalCaseOutstandingOutcomes": True
            },
            "caseBreakdown": {
                "patientDeathEvent": {
                    "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                    "userId": "WERGT-243TRGS-WE4TG-WERGT",
                    "isFinal": True,
                    "eventType": "PatientDied",
                    "dateOfDeath": "2019-03-10T10:01:34.257Z",
                    "timeOfDeath": "11:11:00",
                    "created": "2019-03-10T18:01:34.257Z"
                },
                "otherEvents": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "created": "2019-03-12T10:30:43.019Z",
                            "text": "",
                            "isFinal": True,
                            "eventType": "Other"
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "created": "2019-03-12T10:30:43.019Z",
                        "text": "",
                        "isFinal": True,
                        "eventType": "Other"
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "created": "2019-03-12T10:30:43.019Z",
                        "text": "",
                        "isFinal": False,
                        "eventType": "Other"
                    },
                },
                "preScrutiny": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "created": "2019-03-12T10:30:43.019Z",
                            "medicalExaminerThoughts": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                       "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                                       "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                                       "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                                       "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                                       "consectetur adipiscing elit, sed do eiusmod tempor",
                            "isFinal": True,
                            "eventType": "PreScrutiny",
                            "circumstancesOfDeath": "Expected",
                            "causeOfDeath1a": '',
                            "causeOfDeath1b": '',
                            "causeOfDeath1c": '',
                            "causeOfDeath2": '',
                            "outcomeOfPreScrutiny": "IssueAnMccd",
                            "clinicalGovernanceReview": "Yes",
                            "clinicalGovernanceReviewText": "Palliative care were called too late."
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "created": "2019-03-12T10:30:43.019Z",
                        "medicalExaminerThoughts": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                   "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                                   "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                                   "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                                   "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                                   "consectetur adipiscing elit, sed do eiusmod tempor",
                        "isFinal": True,
                        "eventType": "PreScrutiny",
                        "circumstancesOfDeath": "Expected",
                        "causeOfDeath1a": '',
                        "causeOfDeath1b": '',
                        "causeOfDeath1c": '',
                        "causeOfDeath2": '',
                        "outcomeOfPreScrutiny": "IssueAnMccd",
                        "clinicalGovernanceReview": "Yes",
                        "clinicalGovernanceReviewText": "Palliative care were called too late."
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "created": "2019-03-12T10:30:43.019Z",
                        "medicalExaminerThoughts": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                   "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                                   "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                                   "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                                   "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                                   "consectetur adipiscing elit, sed do eiusmod tempor",
                        "isFinal": False,
                        "eventType": "PreScrutiny",
                        "circumstancesOfDeath": "Expected",
                        "causeOfDeath1a": '',
                        "causeOfDeath1b": '',
                        "causeOfDeath1c": '',
                        "causeOfDeath2": '',
                        "outcomeOfPreScrutiny": "IssueAnMccd",
                        "clinicalGovernanceReview": "Yes",
                        "clinicalGovernanceReviewText": "Palliative care were called too late."
                    }
                },
                "bereavedDiscussion": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "isFinal": True,
                            "eventType": "BereavedDiscussion",
                            "created": "2019-03-12T10:30:43.019Z",
                            "participantFullName": "Jane Doe",
                            "participantRelationship": "Wife",
                            "participantPhoneNumber": "01234 567890",
                            "presentAtDeath": "Yes",
                            "informedAtDeath": "Yes",
                            "dateOfConversation": "2019-04-08T08:31:43.019Z",
                            "discussionUnableHappen": False,
                            "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                 "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                                 "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                                 "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                                 "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                                 "consectetur adipiscing elit, sed do eiusmod tempor",
                            "bereavedDiscussionOutcome": "CouseOfDeathAccepted"
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "isFinal": True,
                        "evenType": "BereavedDiscussion",
                        "created": "2019-03-12T10:30:43.019Z",
                        "participantFullName": "Jane Doe",
                        "participantRelationship": "Wife",
                        "participantPhoneNumber": "01234 567890",
                        "presentAtDeath": "Yes",
                        "informedAtDeath": "Yes",
                        "dateOfConversation": "2019-04-08T08:31:43.019Z",
                        "discussionUnableHappen": False,
                        "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                             "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                             "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                             "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                             "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                             "consectetur adipiscing elit, sed do eiusmod tempor",
                        "bereavedDiscussionOutcome": "CouseOfDeathAccepted"
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "isFinal": False,
                        "evenType": "BereavedDiscussion",
                        "created": "2019-03-12T10:30:43.019Z",
                        "participantFullName": "Jane Doe",
                        "participantRelationship": "Wife",
                        "participantPhoneNumber": "01234 567890",
                        "presentAtDeath": "Yes",
                        "informedAtDeath": "Yes",
                        "dateOfConversation": "2019-04-08T08:31:43.019Z",
                        "discussionUnableHappen": False,
                        "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                             "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                             "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                             "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                             "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                             "consectetur adipiscing elit, sed do eiusmod tempor",
                        "bereavedDiscussionOutcome": "CouseOfDeathAccepted"
                    }
                },
                "meoSummary": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "isFinal": True,
                            "eventType": "MeoSummary",
                            "created": "2019-03-12T10:30:43.019Z",
                            "summaryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                              "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                              "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                              "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                              "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                              "consectetur adipiscing elit, sed do eiusmod tempor"
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "isFinal": True,
                        "eventType": "MeoSummary",
                        "created": "2019-03-12T10:30:43.019Z",
                        "summaryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                          "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                          "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                          "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                          "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                          "consectetur adipiscing elit, sed do eiusmod tempor"
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "isFinal": False,
                        "eventType": "MeoSummary",
                        "created": "2019-03-12T10:30:43.019Z",
                        "summaryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                          "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                          "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                          "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                          "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                          "consectetur adipiscing elit, sed do eiusmod tempor"
                    }
                },
                "qapDiscussion": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "isFinal": True,
                            "eventType": "QapDiscussion",
                            "created": "2019-03-13T10:30:43.019Z",
                            "participantRoll": "Consultant",
                            "participantOrganisation": "A Hospital",
                            "participantPhoneNumber": "01234 567890",
                            "dateOfConversation": "2019-04-08T08:31:43.019Z",
                            "discussionUnableHappen": False,
                            "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                                 "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                                 "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                                 "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                                 "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                                 "consectetur adipiscing elit, sed do eiusmod tempor",
                            "qapDiscussionOutcome": "MccdToBeIssued",
                            "participantName": "Dr G House",
                            "causeOfDeath1a": "",
                            "causeOfDeath1b": "",
                            "causeOfDeath1c": "",
                            "causeOfDeath2": ""
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "isFinal": True,
                        "eventType": "QapDiscussion",
                        "created": "2019-03-13T10:30:43.019Z",
                        "participantRoll": "Consultant",
                        "participantOrganisation": "A Hospital",
                        "participantPhoneNumber": "01234 567890",
                        "dateOfConversation": "2019-04-08T08:31:43.019Z",
                        "discussionUnableHappen": False,
                        "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                             "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                             "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                             "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                             "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                             "consectetur adipiscing elit, sed do eiusmod tempor",
                        "qapDiscussionOutcome": "MccdToBeIssued",
                        "participantName": "Dr G House",
                        "causeOfDeath1a": "",
                        "causeOfDeath1b": "",
                        "causeOfDeath1c": "",
                        "causeOfDeath2": ""
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "isFinal": False,
                        "eventType": "QapDiscussion",
                        "created": "2019-03-13T10:30:43.019Z",
                        "participantRoll": "Consultant",
                        "participantOrganisation": "A Hospital",
                        "participantPhoneNumber": "01234 567890",
                        "dateOfConversation": "2019-04-08T08:31:43.019Z",
                        "discussionUnableHappen": False,
                        "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                             "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                             "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                             "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                             "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                             "consectetur adipiscing elit, sed do eiusmod tempor",
                        "qapDiscussionOutcome": "MccdToBeIssued",
                        "participantName": "Dr G House",
                        "causeOfDeath1a": "",
                        "causeOfDeath1b": "",
                        "causeOfDeath1c": "",
                        "causeOfDeath2": ""
                    }
                },
                "medicalHistory": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "eventType": "MedicalHistory",
                            "isFinal": True,
                            "created": "2019-03-12T10:30:43.019Z",
                            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                    "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                    "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                    "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                    "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                    "consectetur adipiscing elit, sed do eiusmod tempor "
                                    "incididunt ut laborr sit amet, consecteur doloreLorem ipsum "
                                    "dolor sit amet, consectetur adipiscing elit, and alsotext "
                                    "goes here"
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "eventType": "MedicalHistory",
                        "isFinal": True,
                        "created": "2019-03-12T10:30:43.019Z",
                        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                "consectetur adipiscing elit, sed do eiusmod tempor "
                                "incididunt ut laborr sit amet, consecteur doloreLorem ipsum "
                                "dolor sit amet, consectetur adipiscing elit, and alsotext "
                                "goes here"
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "eventType": "MedicalHistory",
                        "isFinal": False,
                        "created": "2019-03-12T10:30:43.019Z",
                        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                                "sed do eiusmod tempor incididunt ut laborr sit amet, "
                                "consecteur dolore Lorem ipsum dolor sit amet, consectetur "
                                "adipiscing elit, sed do eiusmod tempor incididunt ut laborr "
                                "sit amet, consecteur dolore Lorem ipsum dolor sit amet, "
                                "consectetur adipiscing elit, sed do eiusmod tempor "
                                "incididunt ut laborr sit amet, consecteur doloreLorem ipsum "
                                "dolor sit amet, consectetur adipiscing elit, and alsotext "
                                "goes here"
                    }
                },
                "admissionNotes": {
                    "history": [
                        {
                            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                            "userId": "WERGT-243TRGS-WE4TG-WERGT",
                            "notes": '',
                            "isFinal": True,
                            "eventType": "Admission",
                            "admittedDate": "",
                            "admittedTime": "",
                            "immediateCoronerReferral": False,
                            "created": "2019-03-12T10:30:43.019Z",
                        }
                    ],
                    "latest": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "notes": '',
                        "isFinal": True,
                        "eventType": "Admission",
                        "admittedDate": "",
                        "admittedTime": "",
                        "immediateCoronerReferral": False,
                        "created": "2019-03-12T10:30:43.019Z",
                    },
                    "usersDraft": {
                        "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
                        "userId": "WERGT-243TRGS-WE4TG-WERGT",
                        "notes": '',
                        "isFinal": True,
                        "eventType": "Admission",
                        "admittedDate": "",
                        "admittedTime": "",
                        "immediateCoronerReferral": False,
                        "created": "2019-03-12T10:30:43.019Z",
                    }
                }
            },
            "errors": {
                "additionalProp1": [
                    "string"
                ],
                "additionalProp2": [
                    "string"
                ],
                "additionalProp3": [
                    "string"
                ]
            },
            "success": True
        }

    @classmethod
    def get_mock_qap_discussion_form_data(cls):
        return {
            'qap_discussion_id': 1,
            'qap-discussion-doctor': 'other',
            'qap-default__full-name': 'Dr Default',
            'qap-default__role': 'Default Qap',
            'qap-default__organisation': 'Default Org',
            'qap-default__phone-number': 'Default phone',
            'qap-other__full-name': 'Dr Alternate',
            'qap-other__role': 'Alternate Qap',
            'qap-other__organisation': 'Alternate Org',
            'qap-other__phone-number': 'Alternate phone',

            'qap_day_of_conversation': '18',
            'qap_month_of_conversation': '4',
            'qap_year_of_conversation': '2019',
            'qap_time_of_conversation': '11:20',

            'qap-discussion-outcome': 'mccd',
            'qap-dicussion-outcome-decision': 'outcome-decision-1',
        }

    @classmethod
    def get_mock_qap_discussion_draft_data(cls):
        return {
            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
            "userId": "WERGT-243TRGS-WE4TG-WERGT",
            "isFinal": True,
            "eventType": "QapDiscussion",
            "created": "2019-03-13T10:30:43.019Z",
            "participantRoll": "Consultant",
            "participantOrganisation": "A Hospital",
            "participantPhoneNumber": "01234 567890",
            "dateOfConversation": "2019-04-08T08:31:43.019Z",
            "discussionUnableHappen": False,
            "discussionDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            "qapDiscussionOutcome": "MccdToBeIssued",
            "participantName": "Dr G House",
            "causeOfDeath1a": "",
            "causeOfDeath1b": "",
            "causeOfDeath1c": "",
            "causeOfDeath2": ""
        }

    @classmethod
    def get_successful_case_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({"examinationId": "example"}).encode('utf-8')
        return response

    @classmethod
    def get_successful_case_creation_response_with_id_1(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({"examinationId": "1"}).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_case_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_400_BAD_REQUEST
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_case_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_examination_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_case_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_case_index_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_case_index_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_case_index_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_examination_team_post_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_examination_team_post_response(cls):
        response = Response()
        response.status_code = status.HTTP_400_BAD_REQUEST
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_patient_details_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_patient_details_load_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_patient_details_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_patient_details_update_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_patient_details_load_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_patient_details_update_response(cls):
        response = Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_case_breakdown_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_case_breakdown_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_case_breakdown_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_medical_team_load_response(cls, examination_id):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(
            cls.get_medical_team_load_response_content(examination_id=examination_id)).encode('utf-8')
        return response

    @classmethod
    def get_successful_medical_team_update_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_medical_team_load_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_successful_timeline_event_create_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({'eventId': '1'}).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_timeline_event_create_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None).encode('utf-8')
        return response

    @classmethod
    def get_successful_case_outcome_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_case_outcome_response_data()).encode('utf-8')
        return response

    @classmethod
    def get_unsuccessful_case_outcome_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None)
        return response

    @classmethod
    def get_successful_scrutiny_complete_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({"scrutinyConfirmedOn": datetime.now().strftime(API_DATE_FORMAT)})
        return response

    @classmethod
    def get_unsuccessful_scrutiny_complete_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None)
        return response

    @classmethod
    def get_successful_coroner_referral_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({})
        return response

    @classmethod
    def get_unsuccessful_coroner_referral_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None)
        return response

    @classmethod
    def get_successful_outstanding_items_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({})
        return response

    @classmethod
    def get_unsuccessful_outstanding_items_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None)
        return response

    @classmethod
    def get_successful_case_close_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps({})
        return response

    @classmethod
    def get_unsuccessful_case_close_response(cls):
        response = Response()
        response.status_code = status.HTTP_404_NOT_FOUND
        response._content = json.dumps(None)
        return response

    @classmethod
    def get_mock_bereaved_discussion_form_data(cls):
        return {
            'bereaved_event_id': '',
            'bereaved_rep_type': 'alternate-rep',
            'bereaved_existing_rep_name': 'Dominic Hall',
            'bereaved_existing_rep_relationship': 'Uncle',
            'bereaved_existing_rep_phone_number': '1234',
            'bereaved_existing_rep_present_at_death': "no",
            'bereaved_existing_rep_informed': "yes",
            'bereaved_alternate_rep_name': 'Anita West',
            'bereaved_alternate_rep_relationship': 'Sister',
            'bereaved_alternate_rep_phone_number': '1234',
            'bereaved_alternate_rep_present_at_death': "no",
            'bereaved_alternate_rep_informed': "yes",
            'bereaved_day_of_conversation': '24',
            'bereaved_month_of_conversation': '4',
            'bereaved_year_of_conversation': '2019',
            'bereaved_time_of_conversation': '12:40',
            'bereaved_discussion_details': 'The bereaved had some concerns',
            'bereaved_discussion_outcome': 'concerns',
        }

    @classmethod
    def get_mock_bereaved_discussion_draft_data(cls):
        return {
            "eventId": "8FHWRFG-WE4T24TGF-WT4GW3R",
            "userId": "WERGT-243TRGS-WE4TG-WERGT",
            "isFinal": True,
            "eventType": "BereavedDiscussion",
            "created": "2019-03-13T10:30:43.019Z",
            "participantFullName": "Anita West",
            "participantRelationship": "Sister",
            "participantPhoneNumber": "1234",
            "presentAtDeath": "Yes",
            "informedAtDeath": "Yes",
            "dateOfConversation": "2019-04-23T10:47:51.812Z",
            "discussionUnableHappen": False,
            "discussionDetails": "Stop all the clocks, cut off the telephone, "
                                 "Prevent the dog from barking with a juicy bone. "
                                 "Silence the pianos and with muffled drum. "
                                 "Bring out the coffin, let the mourners come.",
            "bereavedDiscussionOutcome": "CouseOfDeathAccepted"
        }


class PeopleMocks:

    @classmethod
    def get_bereaved_representative_response_dict(cls):
        return {
            "fullName": "Jane Doe",
            "relationship": "Wife",
            "phoneNumber": "020 12345678",
            "presentAtDeath": "Yes",
            "informed": "Yes",
            "appointmentDate": NONE_DATE,
            "appointmentTime": ""
        }


class DatatypeMocks:

    @classmethod
    def get_modes_of_disposal_list(cls):
        return {
            "Cremation": 0,
            "Burial": 1,
            "BuriedAtSea": 2,
            "Repatriation": 3
        }
