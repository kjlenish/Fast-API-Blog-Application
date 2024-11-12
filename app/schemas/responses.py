from pydantic import BaseModel
from typing import Union


class SuccessResponse(BaseModel):
    status: str
    data: Union[dict, None]


class ErrorResponse(BaseModel):
    status: str
    message: str
    details: Union[str, None]
