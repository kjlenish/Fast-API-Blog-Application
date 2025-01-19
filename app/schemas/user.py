import re
from fastapi import status
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Union


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str
    
    @field_validator("username")
    def validate_username(cls, username):
        if " " in username:
            raise ValueError("Username must not contain blank space")
        
        return username


    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase character")
        
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase character")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")

        return password


class UserUpdate(BaseModel):
    username: Union[str, None] = None
    email: Union[EmailStr, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    password: Union[str, None] = None
    
    @field_validator("username")
    def validate_username(cls, username):
        if " " in username:
            raise ValueError("Username must not contain blank space")
        
        return username


    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase character")
        
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase character")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")

        return password


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QueryParams(BaseModel):
    skip: int = 0
    limit: int = 10
