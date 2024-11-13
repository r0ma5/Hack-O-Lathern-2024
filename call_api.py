import requests
import sys
import json
import logging

API_ENDPOINT='http://3.239.185.205:8000/image'

logger = logging.getLogger()

session = requests.Session()
session.auth = ('Hack-A-Ton', 'Hack-O-Lathern-2024')

with open(sys.argv[1], 'rb') as f:
    data = f.read()

    files = {'file': data}

    try:
        api_response = session.post(API_ENDPOINT, files=files)
    except Exception as e:
        logger.error(e.args)

    print(json.loads(api_response.text))



