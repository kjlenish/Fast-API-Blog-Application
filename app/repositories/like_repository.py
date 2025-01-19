from sqlmodel import Session, select, and_
from app.models.like import Like


class LikeRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def add(self, like: Like):
        self.session.add(like)
        self.session.commit()
        self.session.refresh(like)
        return like
    
    def remove(self, like: Like):
        self.session.delete(like)
        self.session.commit()
        return True
    
    def has_user_liked_post(self, user_id: int, post_id: int):
        query = select(Like).where(and_(Like.user_id == user_id), (Like.post_id == post_id))
        return self.session.exec(query).first()
    
    def get_post_likes(self, post_id: int):
        query = select(Like).where(Like.post_id == post_id)
        return self.session.exec(query).all()
