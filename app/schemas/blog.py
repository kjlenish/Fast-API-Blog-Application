from pydantic import BaseModel
from datetime import datetime
from typing import Union

class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    published: bool = True


class PostUpdate(BaseModel):
    title: Union[str, None] = None
    content: Union[str, None] = None
    published: Union[bool, None] = True


class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QueryParams(BaseModel):
    skip: int = 0
    limit: int = 10
    q: Union[str, None] = None
    author_id: Union[int, None] = None
