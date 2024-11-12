from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    author_id: int


class PostCreate(PostBase):
    published: bool


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
