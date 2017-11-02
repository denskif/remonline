# ~*~ coding: utf-8 ~*~

import requests

from src.tests.api.lib import KEY_DATA
from src.tests.api.lib.url import TOKEN_URL




def q_post(url, data):
    return requests.post(url, data)

def q_get(url, data):
    return requests.get(url, data)

def q_put(url, data):
    return requests.put(url, data)

def q_status(request):
    return request.status_code

def q_token():
    return requests.post(TOKEN_URL, KEY_DATA)

def new_token():
    response = q_token().json()
    token = 'token'
    return {
        token : response[token]
    }

def get_json(request):
    return request.json()
