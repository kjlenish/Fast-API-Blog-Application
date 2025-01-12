from pydantic import BaseModel
from datetime import datetime
from typing import Union

class PostBase(BaseModel):
    title: str
    content: str
    author_id: int
    published: bool


class PostCreate(PostBase):
    published: bool = True


class PostUpdate(BaseModel):
    title: Union[str, None] = None
    content: Union[str, None] = None
    published: Union[bool, None] = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
