from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from ..utilities import create_access_token, decode_jwt_payload
import urllib.parse
from dotenv import load_dotenv
import requests
import os



load_dotenv()

google_auth = APIRouter(tags=["Google Oauth"])


config = {
  "clientId": os.environ.get("GOOGLE_CLIENT_ID"),
  "clientSecret": os.environ.get("GOOGLE_CLIENT_SECRET"),
  "authUrl": 'https://accounts.google.com/o/oauth2/v2/auth',
  "tokenUrl": 'https://oauth2.googleapis.com/token',
  "redirectUrl": os.environ.get("REDIRECT_URL"),
  "clientUrl": os.environ.get("CLIENT_URL"),
  "tokenSecret": os.environ.get("SECRET_KEY"),
  "tokenExpiration": 36000,
}

authParams = urllib.parse.urlencode({
  "client_id": config["clientId"],
  "redirect_uri": config["redirectUrl"],
  "response_type": 'code',
  "scope": 'openid profile email',
  "access_type": 'offline',
  "state": 'standard_oauth',
  "prompt": 'consent',
})

def getTokenParams(code):
  return urllib.parse.urlencode({
    "client_id": config["clientId"],
    "client_secret": config["clientSecret"],
    "code": code,
    "grant_type": 'authorization_code',
    "redirect_uri": config["redirectUrl"],
    })

@google_auth.get('/auth/url')
async def get_authoization_url():
  return({
  "url": f'{config["authUrl"]}?{authParams}',
  })

@google_auth.get("/auth/token")
async def read_user_item( code : str):
  try:
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code must be provided")


    token_param= getTokenParams(code)
    response = requests.post(f"{config['tokenUrl']}?{token_param}")
    response.raise_for_status()
    data = response.json()
    id_token = data.get('id_token')


    if not id_token:
      raise HTTPException(status_code=400, detail='Auth error')


    # this is wrooooooong 
    user_info = decode_jwt_payload(id_token)
    email = user_info.get('email')
    name = user_info.get('name')
    picture = user_info.get('picture')
    user = {'name': name, 'email': email, 'picture': picture}

    token = create_access_token(data=user)

    response = JSONResponse(content={'user': user, 'token':token})
        
    return response
  except Exception as e:
    raise HTTPException(status_code=500, detail='Server error')

