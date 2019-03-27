import json

from requests.models import Response
from rest_framework import status

from medexCms import settings
from medexCms.utils import NONE_DATE


# Variables/Objects

#### Sessions

AUTH_COOKIES = {
    settings.AUTH_TOKEN_NAME: "c15be3d1-513f-49dc-94f9-47449c1cfeb8",
    settings.ID_TOKEN_NAME: "8a89be6d-70df-4b21-9d6e-82873d7ff1b0"
}

ACCESS_TOKEN = "c15be3d1-513f-49dc-94f9-47449c1cfeb8"

AUTH_TOKEN = {
    "access_token": ACCESS_TOKEN,
    "id_token": "8a89be6d-70df-4b21-9d6e-82873d7ff1b0",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "openid profile email",
}

validate_user_dict = {
    'user_id': '1',
    'first_name': 'Test',
    'last_name': 'User',
    'email_address': 'test.user@email.com',
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
    'userId': '1',
    'firstName': 'Test',
    'lastName': 'User',
    'email': 'test.user@email.com',
}

#### Permissions

CREATED_PERMISSION_ID = 1

PERMISSION_OBJECT = {
      "permissionId": "123-456-789",
      "userId": "abc-def-ghi",
      "locationId": "jkl-mno-pqr",
      "userRole": 0,
  }

USER_PERMISSION_RESPONSE = {
  "permissions": [
      PERMISSION_OBJECT
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

#### Examinations

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


def get_bereaved_examination_form_data():
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
        "hospitalNumber_1": "",
        "hospitalNumber_2": "",
        "hospitalNumber_3": "",
        "genderDetails": '',
        "gender": "male",
        "houseNameNumber": "2",
        "street": "The Street",
        "town": "Anyville",
        "county": "London",
        "postcode": "A1 1NY",
        "country": "",
        "lastOccupation": "",
        "organisationCareBeforeDeathLocationId": "",
        "deathOccuredLocationId": "",
        "modeOfDisposal": "Cremation",
        "funeralDirectors": "",
        "personalAffectsCollected": "yes",
        "personalAffectsDetails": "",
        "dateOfBirth": "",
        "dateOfDeath": "",
        "faithPriority": "True",
        "childPriority": "False",
        "coronerPriority": "False",
        "culturalPriority": "False",
        "otherPriority": "False",
        "priorityDetails": "",
        "completed": "False",
        "coronerStatus": "False",
        "representatives": [
            {
                "full_name": "Jane Doe",
                "relationship": "Wife",
                "phone_number": "020 12345678",
                "present_at_death": "Yes",
                "informed": "Yes",
                "appointment_date": "2019-03-19T14:20:36.609Z",
                "appointment_time": "14:20"
            }
        ]
    }


def get_patient_details_load_response_object():
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


USERS_EXAMINATION_LIST = {
    "examinations": [
        {
            "urgencyScore": 1,
            "givenNames": "John",
            "surname": "Doe",
            "nhsNumber": "123-456-78910",
            "id": "1",
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
            "id": "2",
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
            "id": "3",
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


def get_case_breakdown_response_object():
    return {}


#### People

def get_bereaved_representative():
    return {
      "fullName": "Jane Doe",
      "relationship": "Wife",
      "phoneNumber": "020 12345678",
      "presentAtDeath": "Yes",
      "informed": "Yes",
      "appointmentDate": NONE_DATE,
      "appointmentTime": ""
    }


#### Datatypes

LOAD_MODES_OF_DISPOSAL = {
  "Cremation": 0,
  "Burial": 1,
  "BuriedAtSea": 2,
  "Repatriation": 3
}

# Responses

#### Sessions

SUCCESSFUL_TOKEN_GENERATION = Response()
SUCCESSFUL_TOKEN_GENERATION.status_code = status.HTTP_200_OK
SUCCESSFUL_TOKEN_GENERATION._content = json.dumps(AUTH_TOKEN).encode('utf-8')

SUCCESSFUL_VALIDATE_SESSION = Response()
SUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_200_OK
SUCCESSFUL_VALIDATE_SESSION._content = json.dumps(validate_user_dict).encode('utf-8')

UNSUCCESSFUL_VALIDATE_SESSION = Response()
UNSUCCESSFUL_VALIDATE_SESSION.status_code = status.HTTP_401_UNAUTHORIZED
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

SUCCESSFUL_PERMISSION_LOAD = Response()
SUCCESSFUL_PERMISSION_LOAD.status_code = status.HTTP_200_OK
SUCCESSFUL_PERMISSION_LOAD._content = json.dumps(USER_PERMISSION_RESPONSE).encode('utf-8')

UNSUCCESSFUL_PERMISSION_LOAD = Response()
UNSUCCESSFUL_PERMISSION_LOAD.status_code = status.HTTP_400_BAD_REQUEST
UNSUCCESSFUL_PERMISSION_LOAD._content = json.dumps(None).encode('utf-8')

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

SUCCESSFUL_POST_EXAMINATION_TEAM = Response()
SUCCESSFUL_POST_EXAMINATION_TEAM.status_code = status.HTTP_200_OK
SUCCESSFUL_POST_EXAMINATION_TEAM._content = json.dumps(None).encode('utf-8')

UNSUCCESSFUL_POST_EXAMINATION_TEAM = Response()
UNSUCCESSFUL_POST_EXAMINATION_TEAM.status_code = status.HTTP_400_BAD_REQUEST
UNSUCCESSFUL_POST_EXAMINATION_TEAM._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_PATIENT_DETAILS_LOAD = Response()
SUCCESSFUL_PATIENT_DETAILS_LOAD.status_code = status.HTTP_200_OK
SUCCESSFUL_PATIENT_DETAILS_LOAD._content = json.dumps(get_patient_details_load_response_object()).encode('utf-8')

UNSUCCESSFUL_PATIENT_DETAILS_LOAD = Response()
UNSUCCESSFUL_PATIENT_DETAILS_LOAD.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_PATIENT_DETAILS_LOAD._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_PATIENT_DETAILS_UPDATE = Response()
SUCCESSFUL_PATIENT_DETAILS_UPDATE.status_code = status.HTTP_200_OK
SUCCESSFUL_PATIENT_DETAILS_UPDATE._content = json.dumps(get_patient_details_load_response_object()).encode('utf-8')

UNSUCCESSFUL_PATIENT_DETAILS_UPDATE = Response()
UNSUCCESSFUL_PATIENT_DETAILS_UPDATE.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
UNSUCCESSFUL_PATIENT_DETAILS_UPDATE._content = json.dumps(None).encode('utf-8')

SUCCESSFUL_LOAD_CASE_BREAKDOWN = Response()
SUCCESSFUL_LOAD_CASE_BREAKDOWN.status_code = status.HTTP_200_OK
SUCCESSFUL_LOAD_CASE_BREAKDOWN._content = json.dumps(get_case_breakdown_response_object()).encode('utf-8')

UNSUCCESSFUL_LOAD_CASE_BREAKDOWN = Response()
UNSUCCESSFUL_LOAD_CASE_BREAKDOWN.status_code = status.HTTP_404_NOT_FOUND
UNSUCCESSFUL_LOAD_CASE_BREAKDOWN._content = json.dumps(None).encode('utf-8')
