from fastapi import File, UploadFile, HTTPException, FastAPI
import requests, os, json
import uvicorn

app = FastAPI()

params = {
  'models': 'text,genai',
  'api_user': os.getenv("SIGHTENGINE_USER"),
  'api_secret': os.getenv("SIGHTENGINE_SECRET"),
}

@app.post("/test/")
async def create_upload_file(file: UploadFile):
    data = await file.read()
    files = { 'media': data }
    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
    return json.loads(r.text)


uvicorn.run(app)
