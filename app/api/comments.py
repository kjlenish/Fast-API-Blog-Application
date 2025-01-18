from fastapi import APIRouter, Depends, status
from typing import Annotated, Any, List, Union
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.comment import CommentBase, CommentResponse, CommentUpdate, QueryParams
from app.services.comment_service import CommentService


router = APIRouter(
    tags=["Comments"]
    )


@router.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
def add_new_comment(current_user: UserDep, session: SessionDep, comment: CommentBase, post_id: int):
    comment_service = CommentService(session)
    new_comment = comment_service.create_comment(current_user.id, post_id, comment)
    return new_comment


@router.get("/posts/{post_id}/comments", status_code=status.HTTP_200_OK, response_model=Union[List[CommentResponse], Any])
def get_post_comments(current_user: UserDep, session: SessionDep, params: Annotated[QueryParams, Depends()], post_id: int):
    comment_service = CommentService(session)
    comments = comment_service.get_comment(post_id=post_id, user_id=params.user_id)
    return comments


@router.get("/comments/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse)
def get_comment(current_user: UserDep, session: SessionDep, comment_id: int):
    comment_service = CommentService(session)
    comment = comment_service.get_comment(comment_id=comment_id)
    return comment


@router.patch("/comments/{comment_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse)
def update_comment(current_user: UserDep, session: SessionDep, comment_id: int, comment: CommentUpdate):
    comment_service = CommentService(session)
    updated_comment = comment_service.update_comment(comment_id, comment)
    return updated_comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(current_user: UserDep, session: SessionDep, comment_id: int):
    comment_service = CommentService(session)
    deleted_comment = comment_service.delete_comment(comment_id)
    return deleted_comment
