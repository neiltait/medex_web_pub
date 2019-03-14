import requests


class MedexRequest:

    @classmethod
    def get(cls, auth_token, url):
        headers = {
            'authorization': 'bearer ' + auth_token
        }
        return requests.get(url, headers=headers)

    @classmethod
    def post(cls, auth_token, url, data):
        headers = {
            'authorization': 'bearer ' + auth_token
        }
        return requests.post(url, data=data, headers=headers)
