from typing import Annotated
from fastapi import FastAPI, UploadFile, Request, Response, status
import requests, json, logging, uvicorn, os

logger = logging.getLogger('uvicorn.error')
app = FastAPI()

API_ENDPOINT = 'https://api.sightengine.com/1.0/check.json'

API_PARAMS = {
    'models': 'text,genai',
    'api_user': os.environ['SIGHTENGINE_USER'],
    'api_secret': os.environ['SIGHTENGINE_SECRET']
}

@app.post('/image')
async def inspect_image(request: Request, file: UploadFile, response: Response):
    logger.info(f'{request.client.host}:{request.client.port} - "POST /image"')
    logger.info('Getting image upload...')
    try:
        image = await file.read()
    except Exception as e:
        logger.info(f'Error reading upload file - {e.args}')
        return {'message': 'Error reading image', 'error': True}

    if len(image) == 0:
        logger.info('Upload file is empty')
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': 'Image file is empty', 'error': True}

    files = {'media': image}
    logger.info('File loaded')

    logger.info('Calling sightengine API...')
    try:
        api_response = requests.post(API_ENDPOINT, files=files, data=API_PARAMS)
    except Exception as e:
        logger.info(f'Error - {e.args}')
        return {'message': 'Error occurred when calling Sightengine API', 'error': True}
    logger.info('Received API response')

    if api_response.status_code != 200:
        logger.error('Received response from Sightengine API but operation was unsuccessful')
        logger.info(api_response.text)
        return {'message': 'Operation was unsuccessful', 'error': True}
    
    logger.info('Operation was successful')

    return {'message': 'Image processed successfully', 'error': False, 'data': json.loads(api_response.text)}

uvicorn.run(app)