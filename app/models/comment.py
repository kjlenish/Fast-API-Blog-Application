from typing import Union
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    
    id: Union[int, None] = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    
    parent_id: Union[int, None] = Field(nullable=True, default=None, foreign_key="comments.id", ondelete="CASCADE")
    
    user_id: int = Field(nullable=False, foreign_key="users.id", index=True, ondelete="CASCADE")
    post_id: int = Field(nullable=False, foreign_key="posts.id", index=True, ondelete="CASCADE")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    user: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")
    
    parent: Union["Comment", None] = Relationship(back_populates="replies", sa_relationship_kwargs={"remote_side": "Comment.id"}, cascade_delete=True)
    replies: list["Comment"] = Relationship(back_populates="parent")

    
    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
