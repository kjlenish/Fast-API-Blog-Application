from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from app.core.config import settings
from app.core.security import authenticate_user, create_access_token
from app.dependencies.auth import get_current_user
from app.dependencies.database import SessionDep
from app.models.user import User
from app.schemas.auth import TokenResponse


router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
    )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_202_ACCEPTED)
async def login(session:SessionDep, login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(session, login_form.username, login_form.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "success", "message": "Logged out successfully"}
