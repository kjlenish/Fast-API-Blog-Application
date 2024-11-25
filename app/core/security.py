import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing import Annotated
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.schemas.auth import TokenData
from app.core.exceptions import credentials_exception


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_passed):
    return pwd_context.verify(plain_password, hashed_passed)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = settings.access_token_expire_minutes):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_credential = payload.get("sub")
        if user_credential is None:
            raise credentials_exception
        
        token_data = TokenData(user_credential)
        return token_data
    
    except InvalidTokenError:
        raise credentials_exception
