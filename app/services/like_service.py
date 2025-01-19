from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.models.like import Like
from app.repositories.blog_repository import BlogRepository
from app.repositories.like_repository import LikeRepository
from app.repositories.user_repository import UserRepository
from app.schemas.like import LikeBase


class LikeService:
    def __init__(self, session: Session):
        self.like_repo = LikeRepository(session)
    
    def like_post(self, like: LikeBase):
        user_repo = UserRepository(self.like_repo.session)
        user = user_repo.get_by_id(like.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        blog_repo = BlogRepository(self.like_repo.session)
        post = blog_repo.get_by_id(like.post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if self.like_repo.has_user_liked_post(**like.model_dump()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already liked the post")
        
        new_like = Like(**like.model_dump())
        return self.like_repo.add(new_like)
    
    def unlike_post(self, like: LikeBase):
        user_repo = UserRepository(self.like_repo.session)
        user = user_repo.get_by_id(like.user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        blog_repo = BlogRepository(self.like_repo.session)
        post = blog_repo.get_by_id(like.post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        user_like = self.like_repo.has_user_liked_post(**like.model_dump())
        if user_like is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has not liked the post")
        
        return self.like_repo.remove(user_like)
    
    def get_post_likes(self, post_id: int, user_id: int = None):
        blog_repo = BlogRepository(self.like_repo.session)
        post = blog_repo.get_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if user_id:
            user_repo = UserRepository(self.like_repo.session)
            user = user_repo.get_by_id(user_id)
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
            post = self.like_repo.has_user_liked_post(user_id, post_id)
            if post:
                return [jsonable_encoder(post)]
            return []
        
        return self.like_repo.get_post_likes(post_id)
