from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.comment import CommentBase, CommentResponse, CommentUpdate, QueryParams
from app.schemas.response import SuccessResponse
from app.services.comment_service import CommentService
from app.utils.response_helpers import success_response


router = APIRouter(
    tags=["Comments"]
    )


@router.post("/posts/{post_id}/comments", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def add_new_comment(current_user: UserDep, session: SessionDep, comment: CommentBase, post_id: int):
    comment_service = CommentService(session)
    new_comment = comment_service.create_comment(current_user.id, post_id, comment)
    comment_response = CommentResponse.model_validate(new_comment)
    return await success_response(comment_response)


@router.get("/posts/{post_id}/comments", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_post_comments(current_user: UserDep, session: SessionDep, params: Annotated[QueryParams, Depends()], post_id: int):
    comment_service = CommentService(session)
    comments = comment_service.get_comment(post_id=post_id, user_id=params.user_id)
    
    if comments:
        comment_response = [CommentResponse.model_validate(comment) for comment in comments]
    else:
        comment_response = []
    
    return await success_response(comment_response)


@router.get("/comments/{comment_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_comment(current_user: UserDep, session: SessionDep, comment_id: int):
    comment_service = CommentService(session)
    comment = comment_service.get_comment(comment_id=comment_id)
    comment_response = CommentResponse.model_validate(comment)
    return await success_response(comment_response)


@router.patch("/comments/{comment_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def update_comment(current_user: UserDep, session: SessionDep, comment_id: int, comment: CommentUpdate):
    comment_service = CommentService(session)
    updated_comment = comment_service.update_comment(comment_id, comment)
    comment_response = CommentResponse.model_validate(updated_comment)
    return await success_response(comment_response)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(current_user: UserDep, session: SessionDep, comment_id: int):
    comment_service = CommentService(session)
    deleted_comment = comment_service.delete_comment(comment_id)
    return deleted_comment
