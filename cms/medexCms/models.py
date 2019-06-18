import json

import requests


class MedexRequest:

    @classmethod
    def get(cls, auth_token, url, params={}):
        headers = {
            'authorization': 'bearer ' + auth_token
        }
        return requests.get(url, headers=headers, params=params, verify=False)

    @classmethod
    def post(cls, auth_token, url, data={}):
        headers = {
            'authorization': 'bearer ' + auth_token,
            'content-type': 'application/json-patch+json'
        }
        return requests.post(url, data=data, headers=headers, verify=False)

    @classmethod
    def put(cls, auth_token, url, data={}):
        headers = {
            'authorization': 'bearer ' + auth_token,
            'content-type': 'application/json-patch+json'
        }
        return requests.put(url, data=json.dumps(data), headers=headers, verify=False)
