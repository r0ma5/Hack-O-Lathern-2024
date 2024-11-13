import exifread
from fastapi import File, UploadFile, HTTPException, FastAPI
import requests, os, json
import uvicorn
from PIL import Image
from io import BytesIO, StringIO


app = FastAPI()

params = {
  'models': 'text,genai',
  'api_user': os.getenv("SIGHTENGINE_USER"),
  'api_secret': os.getenv("SIGHTENGINE_SECRET"),
}

@app.post("/test/")
async def create_upload_file(file: UploadFile):
    image_tags = {}
    data = await file.read()

    tags = {}
    tags = exifread.process_file(BytesIO(data))

    for tag in tags:
        if tag.startswith('JPEGThumbnail'):
            continue
#        print("{tag}: {value}".format(tag=tag, value=tags.get(tag)))
        image_tags[tag] = tags.get(tag)
    print(image_tags)
    files = { 'media': data }
    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
    return {
        'ai_screening': json.loads(r.text),
        'exif_tags': image_tags
    }


uvicorn.run(app)
