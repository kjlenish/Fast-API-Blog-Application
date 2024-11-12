from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str
    parent_id: int
    user_id: int
    post_id: int


class CommentCreate(CommentBase):
    pass
    
    
class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
