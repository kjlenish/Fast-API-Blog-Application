from fastapi import APIRouter, Depends
from app.database import SessionDep
from app.services.user_services import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, QueryParams
from typing import Annotated, List, Any, Union


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
    )


@router.post("/", response_model=UserResponse)
async def create_user(db: SessionDep, user: UserCreate):
    print(user)
    user_service = UserService(db)
    new_user = user_service.create_user(user)
    return new_user


@router.get("/", response_model=Union[List[UserResponse], Any])
async def get_users(db: SessionDep, params: Annotated[QueryParams, Depends()]):
    user_service = UserService(db)
    users = user_service.get_users(params.skip, params.limit)
    return users


@router.get("/{user_id}/", response_model=UserResponse)
async def get_user(db: SessionDep, user_id: int):
    user_service = UserService(db)
    user = user_service.get_users(id = user_id)
    return user


@router.patch("/{user_id}/", response_model=UserResponse)
async def update_user(db: SessionDep, user_id: int, user: UserUpdate):
    user_service = UserService(db)
    new_user = user_service.update_user(user_id, user)
    return new_user


@router.delete("/{user_id}/")
async def delete_user(db: SessionDep, user_id: int):
    user_service = UserService(db)
    new_user = user_service.delete_user(user_id)
    return new_user
