from fastapi import Depends
from typing import Annotated
from app.core.exceptions import credentials_exception
from app.core.security import decode_access_token
from app.dependencies.database import SessionDep
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenData


async def get_current_user(session: SessionDep, token_data: Annotated[TokenData, Depends(decode_access_token)]):
    user_repo = UserRepository(session)
    user = user_repo.get_by_credential(token_data.user_credential)
    
    if user is None:
        raise credentials_exception
    
    return user


UserDep = Annotated[User, Depends(get_current_user)]
