from pydantic import BaseModel, EmailStr
from typing import Union


class TokenData(BaseModel):
    user_credential: Union[str, EmailStr]
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(TokenData):
    password: str
