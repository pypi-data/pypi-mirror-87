import os
import requests
import json


API_URL = os.getenv('GADM_API_URL')
API_KEY = os.getenv('GADM_API_KEY')
HEADERS = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY,
}


def id_to_level(id: str): return id.count('.')


def exec_request(gid: str, **kwargs):
    return requests.post(f"{API_URL}/{id_to_level(gid)}", json.dumps(kwargs), headers=HEADERS).json() if API_URL else {}
