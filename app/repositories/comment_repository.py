from sqlmodel import Session, select, and_
from app.models.comment import Comment
from app.schemas.comment import CommentUpdate


class CommentRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, comment: Comment):
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment
    
    def get_by_post(self, post_id, user_id):
        query= select(Comment).where(Comment.post_id == post_id)
        
        if user_id:
            query = select(Comment).where(and_(Comment.post_id == post_id), (Comment.user_id == user_id))
        
        return self.session.exec(query).all()
    
    def get_by_id(self, id):
        return self.session.get(Comment, id)
    
    def update(self, comment: Comment, data: CommentUpdate):
        setattr(comment, "text", data.text)
        self.session.commit()
        self.session.refresh(comment)
        comment.update_timestamp()
        return comment
    
    def delete(self, comment: Comment):
        self.session.delete(comment)
        self.session.commit()
        return True
