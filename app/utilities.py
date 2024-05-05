from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import base64
import os 
import json 

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt_payload(token:str):
    # Split the token into its three parts: header, payload, signature
    parts = token.split('.')
    
    # JWT payload is the second part
    payload = parts[1]
    
    # Base64 decode the payload
    decoded_payload = base64.urlsafe_b64decode(payload + '===').decode('utf-8')
    
    # Parse the decoded payload as JSON to convert it into a dictionary
    payload_dict = json.loads(decoded_payload)
    
    return payload_dict
