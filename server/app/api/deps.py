from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.repositories.character_repo import CharacterRepository
from app.infrastructure.repositories.event_repo import EventRepository
from app.domain.interfaces.repository import IUserRepository, ICharacterRepository, IEventRepository
from app.domain.entities.user import User

settings = get_settings()
security = HTTPBearer()


def get_user_repo(db: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)


def get_character_repo(db: Session = Depends(get_db)) -> ICharacterRepository:
    return CharacterRepository(db)


def get_event_repo(db: Session = Depends(get_db)) -> IEventRepository:
    return EventRepository(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo: IUserRepository = Depends(get_user_repo),
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
