from django.conf import settings

import requests
import urllib


def create_session(code):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'redirect_uri': '%s/login-callback' % settings.CMS_URL,
        'code': code
    }
    return requests.post('%s%s/v1/token' % (settings.OP_DOMAIN, settings.OP_ISSUER),
                         headers=headers,
                         data=urllib.parse.urlencode(data),
                         auth=(settings.OP_ID, settings.OP_SECRET))


def end_session(cookie):
    return requests.get('%s%s/v1/logout?id_token_hint=%s' % (settings.OP_DOMAIN, settings.OP_ISSUER, cookie))
