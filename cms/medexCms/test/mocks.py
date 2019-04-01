import json

from requests.models import Response
from rest_framework import status

from medexCms import settings
from medexCms.utils import NONE_DATE


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
            'user_id': '1',
            'first_name': 'Test',
            'last_name': 'User',
            'email_address': 'test.user@email.com',
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
            'user_id': None,
            'first_name': None,
            'last_name': None,
            'email_address': None,
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
                'id': '1',
                'name': 'Sofia Skouros',
            },
            {
                'id': '2',
                'name': 'Alex McPherson',
            },
            {
                'id': '3',
                'name': 'Suchi Kandukuri',
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
        response._content = json.dumps({'id': cls.USER_ID}).encode('utf-8')
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
    def get_assigned_medical_team_form_data(cls):
        return {
            'medical_examiner': 'Dr Charles Li',
            'medical_examiners_officer': 'Erica Barber',
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
    def get_medical_team_load_response_content(cls):
        return {
            "consultantResponsible": {
                "name": "Peter Hipkiss",
                "role": "Oncologist",
                "organisation": "St Thomas's hospital",
                "phone": "12345",
                "notes": ""
            },
            "consultantsOther": [],
            "generalPractitioner": {
                "name": "",
                "role": "",
                "organisation": "",
                "phone": "",
                "notes": ""
            },
            "qap": {
                "name": "",
                "role": "",
                "organisation": "",
                "phone": "",
                "notes": ""
            },
            "nursingTeamInformation": "",
            "medicalExaminer": {
                "userId": "string",
                "firstName": "",
                "lastName": "",
                "email": "",
                "userRole": "MedicalExaminerOfficer"
            },
            "medicalExaminerOfficer": {
                "userId": "string",
                "firstName": "",
                "lastName": "",
                "email": "",
                "userRole": "MedicalExaminerOfficer"
            },
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
    def get_case_breakdown_response_content(cls):
        return {
            "patientName": 'John Doe',
            "nhsNumber": '0123-456-789',
            "dateOfDeath": "2019-03-12T00:00:00.000Z",
            "timeOfDeath": "13:00",
            "events": [
                {
                    "latest": {
                        "type": "John Doe died",
                        "user": {
                            "id": '1',
                            "name": 'John Smith',
                            'role': 'MEO'
                        },
                        "createdDate": "2019-03-29T10:48:15.749Z",
                        "body": "DOD 2019-03-12T00:00:00.000Z \nTOD 13:00",
                    },
                    "history": [
                        {
                            "type": "John Doe died",
                            "user": {
                                "id": '1',
                                "name": 'John Smith',
                                'role': 'MEO'
                            },
                            "createdDate": "2019-03-29T10:48:15.749Z",
                            "body": "DOD 2019-03-12T00:00:00.000Z \nTOD 13:00",
                        }
                    ]
                },
                {
                    "latest": {
                        "type": "Admission Notes",
                        "user": {
                            "id": '1',
                            "name": 'John Smith',
                            'role': 'MEO'
                        },
                        "createdDate": "2019-03-31T10:48:15.749Z",
                        "body": "Patient was admitted on 10.03.2019 The length of their last admission was 5 days",
                    },
                    "history": [
                        {
                            "type": "Admission Notes",
                            "user": {
                                "id": '1',
                                "name": 'John Smith',
                                'role': 'MEO'
                            },
                            "createdDate": "2019-03-18T10:48:15.749Z",
                            "body": "Patient was admitted on 10.03.2019 The length of their last admission was 5 days",
                        }
                    ]
                },
                {
                    "latest": {
                        "type": "Medical history",
                        "user": {
                            "id": '1',
                            "name": 'John Smith',
                            'role': 'MEO'
                        },
                        "createdDate": "2019-03-31T10:48:15.749Z",
                        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laborr sit amet, consecteur dolore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laborr sit amet, consecteur dolore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laborr sit amet, consecteur doloreLorem ipsum dolor sit amet, consectetur adipiscing elit, and alsotext goes here",
                    },
                    "history": [
                        {
                            "type": "Medical history",
                            "user": {
                                "id": '1',
                                "name": 'John Smith',
                                'role': 'MEO'
                            },
                            "createdDate": "2019-03-18T10:48:15.749Z",
                            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laborr sit amet, consecteur dolore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laborr sit amet, consecteur dolore Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut laborr sit amet, consecteur doloreLorem ipsum dolor sit amet, consectetur adipiscing elit, and alsotext goes here",
                        }
                    ]
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
    def get_successful_case_creation_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(None).encode('utf-8')
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
    def get_successful_medical_team_load_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_medical_team_load_response_content()).encode('utf-8')
        return response

    @classmethod
    def get_successful_medical_team_update_response(cls):
        response = Response()
        response.status_code = status.HTTP_200_OK
        response._content = json.dumps(cls.get_medical_team_load_response_content()).encode('utf-8')
        return response


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

