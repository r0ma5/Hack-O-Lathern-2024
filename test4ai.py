#!/bin/env python

import requests
import json
import os

params = {
  'models': 'text,genai',
  'api_user': os.getenv("SIGHTENGINE_USER"),
  'api_secret': os.getenv("SIGHTENGINE_SECRET")
}
files = {'media': open('test-image.jpg', 'rb')}
r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

output = json.loads(r.text)
print (output)
