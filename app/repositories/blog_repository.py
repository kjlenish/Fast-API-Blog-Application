from sqlmodel import Session, select, or_
from app.models.blog import Post
from app.schemas.blog import PostUpdate


class BlogRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, post: Post):
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post
    
    def get_all(self, skip, limit, search_pattern, author):
        query = select(Post)
        if search_pattern:
            query = query.where(or_(Post.title.ilike(search_pattern)), (Post.content.ilike(
                search_pattern)))
        
        if author:
            query = query.where(Post.author==author)
        
        return self.session.exec(query.offset(skip).limit(limit)).all()
    
    def get_by_id(self, id):
        return self.session.get(Post, id)
    
    def update(self, post: Post, data: PostUpdate):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(post, key, value)
        self.session.commit()
        self.session.refresh(post)
        post.update_timestamp()
        return post
    
    def delete(self, post: Post):
        self.session.delete(post)
        self.session.commit()
        return True
