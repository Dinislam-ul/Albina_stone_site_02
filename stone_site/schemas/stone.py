# stone_site/schemas/stone.py
from typing import Optional, List
from pydantic import BaseModel, Field


# ------СХЕМЫ МЕДИА --------

class Mediabase(BaseModel):
    url: str
    is_main_media: bool = False

class MediaCreate(Mediabase):
    stone_id: int

class MediaResponse(BaseModel):
    id: int
    stone_id: int
    
    class config:
        from_attributes = True

class MediaLoadResponse(BaseModel):
    status: str = "File was added in base"
    id: int
    url: str
    is_main_media: bool
    stone_id: bool
    

# ------СХЕМЫ КАМНИ --------

class StoneBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(gt=1)
    color: Optional[str] = Field(None, max_length=50)

class StoneCreate(StoneBase):
    user_id: Optional[int] = Field(None)
    add_media: Optional[List[str]] = Field(None)

class StoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    color: Optional[str] = None
    user_id: Optional[int] = None
    add_media: Optional[list[str]] = None

class StoneResponse(StoneBase):
    id: int = Field(description="Уникальный ID камня")
    user_id: Optional[int] = Field(None, description="ID владельца")
    add_media: Optional[List[str]] = Field(None, description="Список URL медиафайлов")

    class Config:
        from_attributes = True 

class StoneListResponse(BaseModel):
    items: List[StoneResponse]
    total: int = Field(..., description="Общее количество камней")
    page: int = Field(1, description="Текущая страница")
    size: int = Field(10, description="Количество на странице")