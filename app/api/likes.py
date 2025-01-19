from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.like import LikeBase, LikeResponse, QueryParams
from app.schemas.response import SuccessResponse
from app.services.like_service import LikeService
from app.utils.response_helpers import success_response


router = APIRouter(
    tags=["Likes"]
    )


@router.post("/posts/{post_id}/likes", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def like_post(current_user: UserDep, session: SessionDep, post_id: int):
    like = LikeBase(user_id=current_user.id ,post_id=post_id)
    like_service = LikeService(session)
    new_like = like_service.like_post(like)
    like_response = LikeResponse.model_validate(new_like)
    return await success_response(like_response)


@router.get("/posts/{post_id}/likes", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_post_likes(current_user: UserDep, session: SessionDep, params: Annotated[QueryParams, Depends()], post_id: int):
    like_service = LikeService(session)
    likes = like_service.get_post_likes(post_id, params.user_id)
    
    if likes:
        like_response = [LikeResponse.model_validate(like) for like in likes]
    else:
        like_response = []
    
    return await success_response(like_response)


@router.delete("/posts/{post_id}/likes", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_post(current_user: UserDep, session: SessionDep, post_id: int):
    like = LikeBase(user_id=current_user.id ,post_id=post_id)
    like_service = LikeService(session)
    removed_like = like_service.unlike_post(like)
    return removed_like
