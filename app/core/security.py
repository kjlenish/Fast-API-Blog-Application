import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing import Annotated
from app.core.config import settings
from app.core.exceptions import credentials_exception
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def authenticate_user(session, user_name, password):
    user_repo = UserRepository(session)
    user = user_repo.get_by_credential(user_name)
    if user is None:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user


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
        
        token_data = TokenData(user_credential=user_credential)
        return token_data
    
    except InvalidTokenError:
        raise credentials_exception
