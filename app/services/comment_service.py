from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.comment import Comment
from app.repositories.blog_repository import BlogRepository
from app.repositories.comment_repository import CommentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.comment import CommentBase, CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, session: Session):
        self.comment_repo = CommentRepository(session)
    
    def create_comment(self, user_id: int, post_id: int, comment: CommentBase):
        user_repo = UserRepository(self.comment_repo.session)
        user = user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
        
        blog_repo = BlogRepository(self.comment_repo.session)
        post = blog_repo.get_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if comment.parent_id:
            parent_comment = self.comment_repo.get_by_id(comment.parent_id)
            if parent_comment.parent_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot reply to child comment")
            if parent_comment.post_id != post_id:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Parent comment belongs to a different post")
        
        comment = CommentCreate(user_id=user_id, post_id=post_id, parent_id=comment.parent_id, text=comment.text)
        new_comment = Comment(**comment.model_dump())
        return self.comment_repo.create(new_comment)
    
    def get_comment(self, comment_id: int = None, post_id: int = None, user_id: int = None):
        if comment_id:
            comment = self.comment_repo.get_by_id(comment_id)
        
        else:
            blog_repo = BlogRepository(self.comment_repo.session)
            post = blog_repo.get_by_id(post_id)
            if post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

            if user_id:
                user_repo = UserRepository(self.comment_repo.session)
                user = user_repo.get_by_id(user_id)
                if user is None:
                    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
            
            comment = self.comment_repo.get_by_post(post_id, user_id)
        
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return comment
    
    def update_comment(self, id: int, data: CommentUpdate):
        comment = self.comment_repo.get_by_id(id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
        return self.comment_repo.update(comment, data)

    def delete_comment(self, id: int):
        comment = self.comment_repo.get_by_id(id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
        return self.comment_repo.delete(comment)
