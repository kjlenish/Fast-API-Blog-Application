from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.blog import Post
from app.repositories.blog_repository import BlogRepository
from app.repositories.user_repository import UserRepository
from app.schemas.blog import PostCreate, PostUpdate


class BlogService:
    def __init__(self, session: Session):
        self.blog_repo = BlogRepository(session)
    
    def create_post(self, author_id: int, post: PostCreate):
        user_repo = UserRepository(self.blog_repo.session)
        author = user_repo.get_by_id(author_id)
        if author is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Author not found")
        
        post_dict = post.model_dump()
        post_dict["author_id"] = author_id
        
        new_post = Post(**post_dict)
        return self.blog_repo.create(new_post)
    
    def get_post(self, skip: int = 0, limit: int = 10, q: str = None, author_id: int = None, id: int = None):
        if id:
            post = self.blog_repo.get_by_id(id)
            
            if post is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Post not found")
            else:
                return post
        
        else:
            if q:
                q = f"%{q}%"
            
            if author_id:
                user_repo = UserRepository(self.blog_repo.session)
                author = user_repo.get_by_id(author_id)
            else:
                author = None
            
            return self.blog_repo.get_all(skip, limit, q, author)
    
    def update_post(self, post_id: int, updated_post: PostUpdate):
        post = self.blog_repo.get_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return self.blog_repo.update(post, updated_post)
    
    def delete_post(self, post_id: int):
        post = self.blog_repo.get_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return self.blog_repo.delete(post)
