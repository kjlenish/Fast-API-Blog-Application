from fastapi import APIRouter, Depends, status
from typing import Annotated, Any, List, Union
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.blog import PostCreate, PostResponse, PostUpdate, QueryParams
from app.services.blog_service import BlogService


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(current_user: UserDep, session: SessionDep, post: PostCreate):
    blog_service = BlogService(session)
    new_post = blog_service.create_post(post)
    return new_post


@router.get("/", response_model=Union[List[PostResponse], Any], status_code=status.HTTP_200_OK)
def get_posts(current_user: UserDep, session: SessionDep, params: Annotated[QueryParams, Depends()]):
    blog_service =BlogService(session)
    posts = blog_service.get_post(**params.model_dump())
    return posts


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(current_user: UserDep, session: SessionDep, post_id: int):
    blog_service = BlogService(session)
    post = blog_service.get_post(id=post_id)
    return post


@router.patch("/{post_id}", response_model=PostResponse, status_code=status.HTTP_202_ACCEPTED)
def update_post(current_user: UserDep, session: SessionDep, post_id: int, post: PostUpdate):
    blog_service = BlogService(session)
    updated_post = blog_service.update_post(post_id, post)
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(current_user: UserDep, session: SessionDep, post_id: int):
    blog_service = BlogService(session)
    deleted_post = blog_service.delete_post(post_id)
    return deleted_post
