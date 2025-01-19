from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from app.schemas.response import ErrorResponse


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    details = {
        "url": str(request.url),
        "method": str(request.method),
        "query_params": dict(request.query_params),
        "headers": {k: v for k, v in request.headers.items() if k.lower() not in ["authorization", "cookie"]},        
    }
    
    error_response = ErrorResponse(
        message=exc.detail, details=details, timestamp=str(datetime.utcnow().isoformat())
        )
    
    return JSONResponse(
        content=error_response.model_dump(),
        status_code=exc.status_code
    )
