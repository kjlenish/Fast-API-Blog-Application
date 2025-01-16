from fastapi import APIRouter, Depends, status
from typing import Annotated, Any, List, Union
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, QueryParams


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
    )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user: UserCreate):
    user_service = UserService(session)
    new_user = user_service.create_user(user)
    return new_user


@router.get("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(current_user: UserDep):
    return current_user


@router.get("/all", response_model=Union[List[UserResponse], Any], status_code=status.HTTP_200_OK)
async def get_all_users(session: SessionDep, current_user: UserDep, params: Annotated[QueryParams, Depends()]):
    user_service = UserService(session)
    users = user_service.get_user(params.skip, params.limit)
    return users


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(session: SessionDep, current_user: UserDep, user_id: int):
    user_service = UserService(session)
    user = user_service.get_user(id = user_id)
    return user


@router.patch("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(session: SessionDep, current_user: UserDep, user: UserUpdate):
    user_service = UserService(session)
    updated_user = user_service.update_user(current_user.id, user)
    return updated_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: SessionDep, current_user: UserDep):
    user_service = UserService(session)
    deleted_user = user_service.delete_user(current_user.id)
    return deleted_user
