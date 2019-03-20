import requests


class MedexRequest:

    @classmethod
    def get(cls, auth_token, url):
        headers = {
            'authorization': 'bearer ' + auth_token
        }
        return requests.get(url, headers=headers)

    @classmethod
    def post(cls, auth_token, url, data={}):
        headers = {
            'authorization': 'bearer ' + auth_token,
            'content-type': 'application/json-patch+json'
        }
        return requests.post(url, data=data, headers=headers)

    @classmethod
    def put(cls, auth_token, url, data={}):
        headers = {
            'authorization': 'bearer ' + auth_token,
            'content-type': 'application/json-patch+json'
        }
        return requests.put(url, data=data, headers=headers)
