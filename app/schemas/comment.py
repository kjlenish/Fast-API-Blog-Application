from pydantic import BaseModel
from datetime import datetime
from typing import Union


class CommentBase(BaseModel):
    text: str
    parent_id: Union[int, None] = None


class CommentCreate(CommentBase):
    user_id: int
    post_id: int


class CommentUpdate(BaseModel):
    text: str

    
class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class QueryParams(BaseModel):
    user_id: Union[int, None] = None
