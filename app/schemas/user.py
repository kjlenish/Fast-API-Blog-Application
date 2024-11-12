from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    first_name: str
    last_name: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
