from pydantic import BaseModel
from datetime import datetime
from typing import Union


class LikeBase(BaseModel):
    user_id: int
    post_id: int


class LikeResponse(LikeBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class QueryParams(BaseModel):
    user_id: Union[int, None] = None
