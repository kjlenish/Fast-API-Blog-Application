from pydantic import BaseModel
from typing import Union, Any


class SuccessResponse(BaseModel):
    status: str = "success"
    data: Union[dict, Any]


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Union[str, Any] = None
    timestamp: str
