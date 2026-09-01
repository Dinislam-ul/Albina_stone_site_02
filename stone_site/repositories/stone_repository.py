# stone_site/repositories/stone_repository.py
from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from stone_site.models.stones import Media, User, Stone
from stone_site.repositories.dto import *



class StoneRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, stone_dto: StoneCreateDTO) -> StoneResponseDTO:
        if stone_dto.user_id:
            user = await self.db.get(User, stone_dto.user_id)
            if not user:
                raise ValueError(f"User with id {stone_dto.user_id} not found")
        new_stone = Stone(
            title=stone_dto.title,
            description=stone_dto.description,
            price=stone_dto.price,
            color=stone_dto.color,
            user_id=stone_dto.user_id
        )
        self.db.add(new_stone)
        await self.db.commit()
        await self.db.refresh(new_stone)
        return StoneResponseDTO.from_model(new_stone)


    async def get_by_id(self, stone_id: int) -> Optional[StoneResponseDTO]:
        result = await self.db.execute(select(Stone).where(Stone.id == stone_id))
        stone = result.scalar_one_or_none()
        if stone:
            return StoneResponseDTO.from_model(stone)
        return None

    async def get_all(self) -> List[StoneResponseDTO]:
        result = await self.db.execute(select(Stone))
        stones = result.scalars().all()
        return [StoneResponseDTO.from_model(stone) for stone in stones]
    

    async def get_by_user(self, user_id: int) -> List[StoneResponseDTO]:
        result = await self.db.execute(
            select(Stone).where(Stone.user_id == user_id))
        stones = result.scalars().all()
        return [StoneResponseDTO.from_model(stone) for stone in stones]

    async def update(self,stone_id: int,stone_dto: StoneUpdateDTO) -> Optional[StoneResponseDTO]:
        stone = await self.db.get(Stone, stone_id)
        if not stone:
            return None
        if stone_dto.user_id is not None:
            user = await self.db.get(User, stone_dto.user_id)
            if not user:
                raise ValueError(f"User with id {stone_dto.user_id} not found")
        update_data = stone_dto.__dict__
        for key, value in update_data.items():
            if value is not None and hasattr(stone, key):
                setattr(stone, key, value)
        await self.db.commit()
        await self.db.refresh(stone)
        return StoneResponseDTO.from_model(stone)


    async def delete(self, stone_id: int) -> bool:
        stone = await self.db.get(Stone, stone_id)
        if not stone:
            return False
        await self.db.delete(stone)
        await self.db.commit()
        return True


# ===== МЕТОДЫ ДЛЯ МЕДИА =====

    async def create_media(self, media_data: MediaCreateDTO) -> Media:
        media = Media(
            stone_id=media_data.stone_id,
            url=media_data.url,
            is_main_media = media_data.is_main_media
        )
        self.db.add(media)
        await self.db.commit()
        await self.db.refresh(media)
        return media

    async def get_media_by_id(self, media_id: int) -> Optional[Media]:
        return await self.db.get(Media, media_id)

   