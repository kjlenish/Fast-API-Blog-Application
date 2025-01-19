from fastapi import APIRouter, Depends, status
from typing import Annotated
from app.dependencies.auth import UserDep
from app.dependencies.database import SessionDep
from app.schemas.blog import PostCreate, PostResponse, PostUpdate, QueryParams
from app.schemas.response import SuccessResponse
from app.services.blog_service import BlogService
from app.utils.response_helpers import success_response


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_post(current_user: UserDep, session: SessionDep, post: PostCreate):
    blog_service = BlogService(session)
    new_post = blog_service.create_post(current_user.id, post)
    post_response = PostResponse.model_validate(new_post)
    return await success_response(post_response)


@router.get("/", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_posts(current_user: UserDep, session: SessionDep, params: Annotated[QueryParams, Depends()]):
    blog_service =BlogService(session)
    posts = blog_service.get_post(**params.model_dump())
    
    if posts:
        post_response = [PostResponse.model_validate(post) for post in posts]
    else:
        post_response = []
    
    return await success_response(post_response)


@router.get("/{post_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK)
async def get_post(current_user: UserDep, session: SessionDep, post_id: int):
    blog_service = BlogService(session)
    post = blog_service.get_post(id=post_id)
    post_response = PostResponse.model_validate(post)
    
    return await success_response(post_response)


@router.patch("/{post_id}", response_model=SuccessResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_post(current_user: UserDep, session: SessionDep, post_id: int, post: PostUpdate):
    blog_service = BlogService(session)
    updated_post = blog_service.update_post(post_id, post)
    post_response = PostResponse.model_validate(updated_post)
    return await success_response(post_response)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(current_user: UserDep, session: SessionDep, post_id: int):
    blog_service = BlogService(session)
    deleted_post = blog_service.delete_post(post_id)
    return deleted_post
