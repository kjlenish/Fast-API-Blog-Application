from app.schemas.response import SuccessResponse
from typing import Any

async def success_response(data: Any) -> SuccessResponse:
    return SuccessResponse(data=data)
