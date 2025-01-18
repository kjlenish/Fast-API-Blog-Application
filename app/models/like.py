from typing import Union
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Like(SQLModel, table=True):
    __tablename__ = "likes"
    
    id: Union[int, None] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="users.id", index=True, ondelete="CASCADE")
    post_id: int = Field(nullable=False, foreign_key="posts.id", index=True, ondelete="CASCADE")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    user: "User" = Relationship(back_populates="likes")
    post: "Post" = Relationship(back_populates="likes")



from app.models.user import User
from app.models.blog import Post
from app.models.like import Like

User.update_forward_refs()
Post.update_forward_refs()
Like.update_forward_refs()
