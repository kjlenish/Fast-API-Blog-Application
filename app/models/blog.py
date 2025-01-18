from typing import List, Union
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    id: Union[int, None] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    
    author_id: int = Field(nullable=False, foreign_key="users.id", index=True, ondelete="CASCADE")
    published: bool = Field(default=False)
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    author: "User" = Relationship(back_populates="posts")
    comments: "Comment" = Relationship(back_populates="post", cascade_delete=True)
    likes: List["Like"] = Relationship(back_populates="post", cascade_delete=True)
    
    
    def update_timestamp(self):
        self.updated_at = datetime.utcnow()


from app.models.user import User
from app.models.blog import Post
from app.models.comment import Comment
from app.models.like import Like

User.update_forward_refs()
Post.update_forward_refs()
Comment.update_forward_refs()
Like.update_forward_refs()
