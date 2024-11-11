import re
from fastapi import HTTPException, status
from typing import Union, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr, field_validator
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Union[int, None] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, nullable=False, index=True)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)  
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    posts: List["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: List["Comment"] = Relationship(back_populates="user", cascade_delete=True)
    
    
    @field_validator("username")
    def validate_username(cls, username):
        if " " in username:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username must not contain blank space")
        
        return username


    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password must be at least 8 characters long")
        
        if not re.search(r"[A-Z]", password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password must contain at least one uppercase character")
        
        if not re.search(r"[a-z]", password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password must contain at least one lowercase character")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password must contain at least one special character")

        return password
    
    
    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
