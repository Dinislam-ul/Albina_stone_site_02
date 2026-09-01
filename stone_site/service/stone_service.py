import uuid
from typing import Optional

from fastapi import HTTPException, UploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from stone_site.core.s3_client import s3_client
from stone_site.models import Media, Stone
from stone_site.repositories.dto import *
from stone_site.repositories.stone_repository import StoneRepository
from stone_site.schemas.stone import StoneCreate, StoneUpdate


class StoneService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = StoneRepository(db)

    async def create_stone(self, stone_data: StoneCreate) -> StoneResponseDTO:
        stone_dto = StoneCreateDTO.from_schema(stone_data)
        return await self.repository.create(stone_dto)

    async def get_stone(self, stone_id: int) -> Optional[StoneResponseDTO]:
        result = await self.repository.get_by_id(stone_id)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Stone with id {stone_id} not found"
        )
        return result

    async def get_all_stones(self) -> List[StoneResponseDTO]:
        return await self.repository.get_all()
    

    async def get_user_stones(self, user_id: int) -> List[StoneResponseDTO]:
        return await self.repository.get_by_user(user_id)

    async def update_stone(
        self,
        stone_id: int,
        stone_data: StoneUpdate
    ) -> Optional[StoneResponseDTO]:
        existing = await self.repository.get_by_id(stone_id)
        if not existing:
            raise ValueError(f"Stone with id {stone_id} not found")
        stone_dto = StoneUpdateDTO.from_schema(stone_data)
        return await self.repository.update(stone_id, stone_dto)

    async def delete_stone(self, stone_id: int) -> bool:
        existing = await self.repository.get_by_id(stone_id)
        if not existing:
            raise ValueError(f"Stone with id {stone_id} not found")
        return await self.repository.delete(stone_id)

    
       # ===== МЕТОДЫ ДЛЯ МЕДИА (ФОТО) =====

    async def upload_stone_file(
        self, 
        stone_id: int,
        file: UploadFile,
        is_main_media: bool = False
    ) -> MediaLoadResponse:
        # ШАГ 1: Проверяем существование камня
        query = select(Stone).where(Stone.id == stone_id)
        result = await self.db.execute(query)
        stone = result.scalar_one_or_none()
        
        if not stone:
            raise HTTPException(status_code=404, detail="Stone not found")
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        s3_filename = f"stones/{stone_id}/{uuid.uuid4()}.{file_extension}"
        file_data = await file.read()
        
        try:
            # ШАГ 3: Загружаем файл в S3 (используем метод upload_file из вашего S3Client)
            file_url = s3_client.upload_file(
                file_data=file_data,
                filename=s3_filename,
                content_type=file.content_type or "image/jpeg"
            )
            
            # ШАГ 4: Проверяем, есть ли уже медиа у этого камня
            existing_media_query = select(Media).where(Media.stone_id == stone_id)
            existing_media_result = await self.db.execute(existing_media_query)
            existing_media = existing_media_result.first()
            
            # Если нет ни одного медиа, делаем этот файл главным
            if not existing_media:
                is_main_media = True
            
            # ШАГ 5: Создаем запись медиа в БД
            media = Media(
                stone_id=stone_id,
                url=file_url,
                is_main_media=is_main_media
            )
            self.db.add(media)
            await self.db.commit()
            await self.db.refresh(media)
            
            # ШАГ 6: Если это главное медиа, убираем флаг у остальных
            if is_main_media:
                await self.db.execute(
                    update(Media)
                    .where(Media.stone_id == stone_id)
                    .where(Media.id != media.id)
                    .values(is_main_media=False)
                )
                await self.db.commit()
            
            # ШАГ 7: Возвращаем ответ
            return MediaLoadResponse(
                id=media.id,
                url=media.url,
                is_main_media=media.is_main_media,
                stone_id=media.stone_id,
                message="File uploaded successfully"
            )
            
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    