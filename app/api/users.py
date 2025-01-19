from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.response import SuccessResponse
from app.schemas.user import UserCreate, UserUpdate, UserResponse, QueryParams
from app.services.user_service import UserService
from app.utils.response_helpers import success_response


router = APIRouter(
    prefix="/users", 
    tags=["Users"]
    )


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user: UserCreate):
    user_service = UserService(session)
    new_user = user_service.create_user(user)
    user_response = UserResponse.model_validate(new_user)
    return await success_response(user_response)


@router.get("/", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_current_user(current_user: UserDep):
    user_response = UserResponse.model_validate(current_user)
    return await success_response(user_response)


@router.get("/all", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_all_users(session: SessionDep, current_user: UserDep, params: Annotated[QueryParams, Depends()]):
    user_service = UserService(session)
    users = user_service.get_user(params.skip, params.limit)
    
    if users:
        user_response = [UserResponse.model_validate(user) for user in users]
    else:
        user_response = []
    
    return await success_response(user_response)


@router.get("/{user_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_user(session: SessionDep, current_user: UserDep, user_id: int):
    user_service = UserService(session)
    user = user_service.get_user(id = user_id)
    user_response = UserResponse.model_validate(user)
    return await success_response(user_response)


@router.patch("/", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def update_user(session: SessionDep, current_user: UserDep, user: UserUpdate):
    user_service = UserService(session)
    updated_user = user_service.update_user(current_user.id, user)
    user_response = UserResponse.model_validate(updated_user)
    return await success_response(user_response)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(session: SessionDep, current_user: UserDep):
    user_service = UserService(session)
    deleted_user = user_service.delete_user(current_user.id)
    return deleted_user
