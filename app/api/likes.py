from fastapi import APIRouter, Depends, status
from typing import Annotated, Any, List, Union
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.like import LikeBase, LikeResponse, QueryParams
from app.services.like_service import LikeService


router = APIRouter(
    tags=["Likes"]
    )


@router.post("/posts/{post_id}/likes", status_code=status.HTTP_200_OK, response_model=LikeResponse)
def like_post(current_user: UserDep, session: SessionDep, post_id: int):
    like = LikeBase(user_id=current_user.id ,post_id=post_id)
    like_service = LikeService(session)
    new_like = like_service.like_post(like)
    return new_like


@router.get("/posts/{post_id}/likes", status_code=status.HTTP_200_OK, response_model=Union[List[LikeResponse], Any])
def get_post_likes(current_user: UserDep, session: SessionDep, params: Annotated[QueryParams, Depends()], post_id: int):
    like_service = LikeService(session)
    likes = like_service.get_post_likes(post_id, params.user_id)
    return likes


@router.delete("/posts/{post_id}/likes", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(current_user: UserDep, session: SessionDep, post_id: int):
    like = LikeBase(user_id=current_user.id ,post_id=post_id)
    like_service = LikeService(session)
    removed_like = like_service.unlike_post(like)
    return removed_like
