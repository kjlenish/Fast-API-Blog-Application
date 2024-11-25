from fastapi import APIRouter, Depends, status

from app.dependencies.database import SessionDep
from app.services.user_service import UserService
from app.schemas.auth import TokenResponse
from typing import Annotated, List, Any, Union


router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
    )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_202_ACCEPTED)
async def login():
    pass
