from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


class UserService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)
    
    def create_user(self, user: UserCreate):
        if self.user_repo.check_username_exists(user.username):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Username already exists")
        if self.user_repo.check_email_exists(user.email):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email already exists")
        
        extra_data = {"password": hash_password(user.password)}
        user.__dict__.update(extra_data)
        
        new_user = User(**user.dict())

        return self.user_repo.create(new_user)
    
    def get_users(self, skip: int = 0, limit: int = 10, id: int = None):
        if id:
            user = self.user_repo.get_by_id(id)
            if user is None:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
            else:
                return user
            
        else:
            return self.user_repo.get_all(skip, limit)
    
    def update_user(self, user_id: int, updated_user: UserUpdate):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
        
        if user.username != updated_user.username:
            if self.user_repo.check_username_exists(user.username):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Username already exists")
        
        if user.email != updated_user.email:
            if self.user_repo.check_email_exists(user.email):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Email already exists")
        
        user_data = updated_user.model_dump(exclude_unset=True) 
        extra_data = {}       
        if "password" in user_data:
            extra_data["password"] = hash_password(user_data["password"])
            updated_user.__dict__.update(extra_data)
        return self.user_repo.update(user, updated_user)
    
    def delete_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
        
        return self.user_repo.delete(user)
