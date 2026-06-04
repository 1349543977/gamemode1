from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.interfaces.repository import IUserRepository
from app.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    async def get_by_openid(self, openid: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.openid == openid).first()
        return self._to_entity(model) if model else None

    async def create(self, user: User) -> User:
        model = UserModel(
            openid=user.openid,
            union_id=user.union_id,
            phone=user.phone,
            nickname=user.nickname,
            avatar_url=user.avatar_url,
            platform=user.platform,
            last_login_at=user.last_login_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not model:
            raise ValueError(f"User {user.id} not found")
        model.nickname = user.nickname
        model.avatar_url = user.avatar_url
        model.phone = user.phone
        model.union_id = user.union_id
        model.last_login_at = user.last_login_at
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            openid=model.openid,
            union_id=model.union_id,
            phone=model.phone,
            nickname=model.nickname,
            avatar_url=model.avatar_url,
            platform=model.platform,
            last_login_at=model.last_login_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
