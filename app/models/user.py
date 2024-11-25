from typing import Union, List
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
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
    
    
    def update_timestamp(self):
        self.updated_at = datetime.utcnow()


from app.models.user import User
from app.models.blog import Post
from app.models.comment import Comment

User.update_forward_refs()
Post.update_forward_refs()
Comment.update_forward_refs()
