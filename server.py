import secrets
from typing import Annotated
from fastapi import FastAPI, UploadFile, Request, Response, status
from fastapi import Depends, HTTPException
import requests, json, logging, uvicorn, os
import rule_engine
from fastapi.security import HTTPBasic, HTTPBasicCredentials

ai_generated_image = rule_engine.Rule(
    'ais >= 0.5 and qs < 0.85'
)

modified_image = rule_engine.Rule(
    'ais < 0.1 and qs < 0.85'
)

logger = logging.getLogger('uvicorn.error')


security = HTTPBasic()

app = FastAPI(dependencies=[Depends(security)])

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"Hack-A-Ton"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"Hack-O-Lathern-2024"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

API_ENDPOINT = 'https://api.sightengine.com/1.0/check.json'

API_PARAMS = {
    'models': 'genai,quality',
    'api_user': os.environ['SIGHTENGINE_USER'],
    'api_secret': os.environ['SIGHTENGINE_SECRET']
}

@app.post('/image')
async def inspect_image(request: Request, file: UploadFile, response: Response, dependencies=[Depends(get_current_username)]):
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

    try:
        data = json.loads(api_response.text)
        logger.info(data)
        scoring_data = {
            "id": data.get('media').get('id'),
            "ais": data.get('type').get('ai_generated'),
            "qs": data.get('quality').get('score')
        }
        if ai_generated_image.matches(scoring_data):
            logger.info('{id} - AI generated image: score 1.0'.format(id=scoring_data.get('id')))
            rs = {"score": 1.0}
        elif modified_image.matches(scoring_data):
            logger.info('{id} - Modified image: score 0.5'.format(id=scoring_data.get('id')))
            rs = {"score": 0.5}
        else:
            logger.info('{id} - Good image: score 0.0'.format(id=scoring_data.get('id')))
            rs = {"score": 0.0}
    except Exception as e:
        logger.info(f'Error - {e.args}')
        return {'message': 'Error occurred when parsing Sightengine API output', 'error': True}


    return {'message': 'Image processed successfully', 'error': False, 'data': rs}

uvicorn.run(app, host='0.0.0.0')