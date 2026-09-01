from stone_site.core.database import AsyncSession, get_db
from fastapi import Depends, APIRouter, UploadFile, File, Form
from stone_site.service.stone_service import StoneService
from stone_site.schemas.stone import *
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from stone_site.service.stone_service import StoneService
from stone_site.schemas.stone import *


stone_router = APIRouter(prefix="/stone",tags=["Stone"])


# ===== Эндпоинты =====
# ============================================================
# 1. STONE - CRUD ОПЕРАЦИИ /stone
# ============================================================
@stone_router.get("/{stone_id}", tags=["Stone"],summary="Get info about stone by ID",response_model=StoneResponse )
async def get_stones_catalogy(stone_id: int, db:AsyncSession=Depends(get_db)):
    service = StoneService(db)
    return await service.get_stone(stone_id) 


@stone_router.get("/{user_id}", summary="Get all user's stones", response_model=list[StoneResponse])
async def get_user_stones(user_id: int,db: AsyncSession = Depends(get_db)):
    service = StoneService(db)
    return await service.get_user_stones(user_id)


@stone_router.delete("/{stone_id}", summary="Delete stone by ID")
async def delete_stone(stone_id: int, db: AsyncSession=Depends(get_db)):
    service = StoneService(db)
    return await service.delete_stone(stone_id)


@stone_router.post("/", summary="Create new stone", response_model=StoneResponse)
async def add_stone(stone_data: StoneCreate, db:AsyncSession=Depends(get_db)):
    service=StoneService(db)
    return await service.create_stone(stone_data)


@stone_router.patch("/{stone_id}", summary="Update info aboit stone by ID", response_model=StoneResponse)
async def update_stone(stone_id: int, stone_data: StoneUpdate,db: AsyncSession=Depends(get_db)):
    service = StoneService(db)
    return await service.update_stone(stone_id, stone_data)

# ============================================================
# 2. КАТАЛОГ - ПУБЛИЧНЫЕ ЭНДПОИНТЫ /catalog
# ============================================================

@stone_router.get("/", summary="Get stone catalogy", response_model=List[StoneResponse])
async def get_all_stones(db: AsyncSession = Depends(get_db)):
    service = StoneService(db)
    return await service.get_all_stones()
    


# ===== ЭНДПОИНТЫ ДЛЯ МЕДИА (ФОТО) =====

@stone_router.post("/{stone_id}/media", response_model = MediaLoadResponse)
async def upload_stone_media(
    stone_id: int,
    file: UploadFile = File(...),  # Файл обязателен
    is_main_media: bool = Form(False),  # Параметр из формы (опционально)
    db: AsyncSession = Depends(get_db), # Требуем авторизацию
):
    service = StoneService(db)
    return await service.upload_stone_file(stone_id, file, is_main_media)

