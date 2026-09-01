
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from stone_site.models import User
from stone_site.repositories.dto import UserResponseDTO


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, username: str, email: str, hashed_password: str, is_admin: bool = False) -> UserResponseDTO:
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return UserResponseDTO.from_model(new_user)

    async def get_by_id(self, user_id: int) -> Optional[UserResponseDTO]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            return UserResponseDTO.from_model(user)
        return None

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_model_by_id(self, user_id: int) -> Optional[User]:
        return await self.db.get(User, user_id)