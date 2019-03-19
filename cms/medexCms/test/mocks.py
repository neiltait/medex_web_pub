import json

from requests.models import Response
from rest_framework import status

from medexCms import settings

# Variables/Objects

#### Sessions

AUTH_COOKIES = {
    settings.AUTH_TOKEN_NAME: "c15be3d1-513f-49dc-94f9-47449c1cfeb8",
    settings.ID_TOKEN_NAME: "8a89be6d-70df-4b21-9d6e-82873d7ff1b0"
}

AUTH_TOKEN = {
    "access_token": "c15be3d1-513f-49dc-94f9-47449c1cfeb8",
    "id_token": "8a89be6d-70df-4b21-9d6e-82873d7ff1b0",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "openid profile email",
}

#### Users

CREATED_USER_ID = 1

empty_user = {
    'user_id': None,
    'first_name': None,
    'last_name': None,
    'email_address': None,
}

user_dict = {
    'user_id': '1',
    'first_name': 'Test',
    'last_name': 'User',
    'email_address': 'test.user@email.com',
}

#### Permissions

CREATED_PERMISSION_ID = 1

#### Locations
SUCCESSFUL_TRUST_LOAD = [
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

SUCCESSFUL_REGION_LOAD = [
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

SUCCESSFUL_ME_OFFICES_LOAD = [
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

SUCCESSFUL_MEDICAL_EXAMINERS = [{
        'id': '1',
        'name': 'Dr Alicia Anders',
    }, {
        'id': '2',
        'name': 'Dr Brandon Weatherby',
    }, {
        'id': '3',
        'name': 'Dr Charles Lighterman',
    }, {
        'id': '4',
        'name': 'Dr Subhashine Sanapala',
    }, {
        'id': '5',
        'name': 'Dr Ore Thompson',
    }
]

SUCCESSFUL_MEDICAL_EXAMINERS_OFFICERS = [
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

#### Examintations

CREATED_EXAMINATION_ID = 1


def get_minimal_create_form_data():
    return {
        'last_name': 'Nicks',
        'first_name': 'Matt',
        'gender': 'male',
        'nhs_number_not_known': True,
        'date_of_birth_not_known': True,
        'time_of_death_not_known': True,
        'date_of_death_not_known': True,
        'place_of_death': 1,
        'me_office': 1,
    }


SECONDARY_EXAMINATION_DATA = {
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


def get_bereaved_examination_data():
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


URGENCY_EXAMINATION_DATA = {
    'faith_death': 'yes',
    'coroner_case': 'no',
    'child_death': 'no',
    'cultural_death': 'no',
    'other': 'no',
    'urgency_additional_details': '',
}


def get_medical_team_form_data():
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


def get_assigned_medical_team_form_data():
    return {
        'medical_examiner': 'Dr Charles Li',
        'medical_examiners_officer': 'Erica Barber',
    }


def get_examination_response_object():
    return {
        "id": "1",
        "timeOfDeath": "",
        "givenNames": "John",
        "surname": "Doe",
        "nhsNumber": "123-456-78910",
        "gender": "male",
        "houseNameNumber": "",
        "street": "",
        "town": "",
        "county": "",
        "postcode": "",
        "country": "",
        "lastOccupation": "",
        "organisationCareBeforeDeathLocationId": "",
        "deathOccuredLocationId": "",
        "modeOfDisposal": "",
        "funeralDirectors": "",
        "personalAffectsCollected": "",
        "personalAffectsDetails": "",
        "jewelleryCollected": "",
        "jewelleryDetails": "",
        "dateOfBirth": "",
        "dateOfDeath": "",
        "faithPriority": "False",
        "childPriority": "False",
        "coronerPriority": "False",
        "otherPriority": "False",
        "priorityDetails": "",
        "completed": "False",
        "coronerStatus": "False"
    }


USERS_EXAMINATION_LIST = {
    "examinations": [
        {
            "urgencyScore": 1,
            "givenNames": "John",
            "surname": "Doe",
            "nhsNumber": "123-456-78910",
            "id": "1",
            "timeOfDeath": "10:48",
            "dateOfBirth": "2019-03-18T10:48:15.749Z",
            "dateOfDeath": "2019-03-18T10:48:15.749Z",
            "appointmentDate": "2019-03-18T10:48:15.749Z",
            "appointmentTime": "15:48",
            "lastAdmission": "2019-03-18T10:48:15.749Z",
            "caseCreatedDate": "2019-03-18T10:48:15.749Z"
        },
        {
            "urgencyScore": 0,
            "givenNames": "John",
            "surname": "Doe",
            "nhsNumber": "123-456-78910",
            "id": "1",
            "timeOfDeath": "10:48",
            "dateOfBirth": "2019-03-18T10:48:15.749Z",
            "dateOfDeath": "2019-03-18T10:48:15.749Z",
            "appointmentDate": "2019-03-18T10:48:15.749Z",
            "appointmentTime": "15:48",
            "lastAdmission": "2019-03-18T10:48:15.749Z",
            "caseCreatedDate": "2019-03-18T10:48:15.749Z"
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

# Responses

#### Sessions

SUCCESSFUL_TOKEN_GENERATION = Response()
SUCCESSFUL_TOKEN_GENERATION.status_code = status.HTTP_200_OK
SUCCESSFUL_TOKEN_GENERATION._content = json.dumps(AUTH_TOKEN).encode('utf-8')

SUCCESSFUL_VALIDATE_SESSION = Response()
SUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
SUCCESSFUL_VALIDATE_SESSION._content = json.dumps(user_dict).encode('utf-8')

UNSUCCESSFUL_VALIDATE_SESSION = Response()
UNSUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
UNSUCCESSFUL_VALIDATE_SESSION._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_LOGOUT = Response()
SUCCESSFUL_LOGOUT.status_code = status.HTTP_200_OK

#### Users

SUCCESSFUL_USER_CREATION = Response()
SUCCESSFUL_USER_CREATION.status_code = status.HTTP_200_OK
SUCCESSFUL_USER_CREATION._content = json.dumps({'id': CREATED_USER_ID}).encode('utf-8')

UNSUCCESSFUL_USER_CREATION = Response()
UNSUCCESSFUL_USER_CREATION.status_code = status.HTTP_400_BAD_REQUEST
UNSUCCESSFUL_USER_CREATION._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_LOAD_USER = Response()
SUCCESSFUL_LOAD_USER.status_code = status.HTTP_200_OK
SUCCESSFUL_LOAD_USER._content = json.dumps(user_dict).encode('utf-8')

UNSUCCESSFUL_LOAD_USER = Response()
UNSUCCESSFUL_LOAD_USER.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_LOAD_USER._content = json.dumps(empty_user).encode('utf-8')

SUCCESSFUL_USER_LOOKUP = Response()
SUCCESSFUL_USER_LOOKUP.status_code = status.HTTP_200_OK
SUCCESSFUL_USER_LOOKUP._content = json.dumps(None).encode('utf-8')

UNSUCCESSFUL_USER_LOOKUP = Response()
UNSUCCESSFUL_USER_LOOKUP.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_USER_LOOKUP._content = json.dumps(None).encode('utf-8')

#### Permissions

SUCCESSFUL_PERMISSION_CREATION = Response()
SUCCESSFUL_PERMISSION_CREATION.status_code = status.HTTP_200_OK
SUCCESSFUL_PERMISSION_CREATION._content = json.dumps({'permissionId': CREATED_PERMISSION_ID}).encode('utf-8')

UNSUCCESSFUL_PERMISSION_CREATION = Response()
UNSUCCESSFUL_PERMISSION_CREATION.status_code = status.HTTP_400_BAD_REQUEST
UNSUCCESSFUL_PERMISSION_CREATION._content = json.dumps(None).encode('utf-8')

#### Examintations

SUCCESSFUL_CASE_CREATE = Response()
SUCCESSFUL_CASE_CREATE.status_code = status.HTTP_200_OK
SUCCESSFUL_CASE_CREATE._content = json.dumps(None).encode('utf-8')

UNSUCCESSFUL_CASE_CREATE = Response()
UNSUCCESSFUL_CASE_CREATE.status_code = status.HTTP_400_BAD_REQUEST
UNSUCCESSFUL_CASE_CREATE._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_CASE_LOAD = Response()
SUCCESSFUL_CASE_LOAD.status_code = status.HTTP_200_OK
SUCCESSFUL_CASE_LOAD._content = json.dumps(get_examination_response_object()).encode('utf-8')

UNSUCCESSFUL_CASE_LOAD = Response()
UNSUCCESSFUL_CASE_LOAD.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_CASE_LOAD._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_CASE_INDEX = Response()
SUCCESSFUL_CASE_INDEX.status_code = status.HTTP_200_OK
SUCCESSFUL_CASE_INDEX._content = json.dumps(USERS_EXAMINATION_LIST).encode('utf-8')

UNSUCCESSFUL_CASE_INDEX = Response()
UNSUCCESSFUL_CASE_INDEX.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_CASE_INDEX._content = json.dumps(None).encode('utf-8')
