from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        print("Created")

    def create(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_all(self, skip, limit):
        query = select(User).offset(skip).limit(limit)
        return self.session.exec(query).all()
    
    def get_by_id(self, id):
        return self.session.get(User, id)
    
    def check_username_exists(self, username):
        query = select(User).where(User.username==username)
        user = self.session.exec(query).first()
        return bool(user)
    
    def check_email_exists(self, email):
        query = select(User).where(User.email==email)
        user = self.session.exec(query).first()
        return bool(user)
    
    def update(self, user: User, data: UserCreate):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        user.update_timestamp()
        return user
    
    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()
        return True
