import requests
import json
import sys

params = {
  'models': 'text,genai',
  'api_user': os.getenv("SIGHTENGINE-USER"),
  'api_secret': os.getenv("SIGHTENGINE-SECRET")
}
files = {'media': open('test-image.jpg', 'rb')}
r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

output = json.loads(r.text)
print (output)