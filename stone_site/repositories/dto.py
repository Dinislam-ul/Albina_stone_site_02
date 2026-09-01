# stone_site/repositories/dto.py
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from stone_site.schemas.stone import *
from stone_site.models.stones import Stone


# ===== DTO ДЛЯ МЕДИА (ФОТО) =====
class MediaDTO(BaseModel):
    id: int
    stone_id: int
    url: str
    is_main_media: bool

    class Config:
        from_attributes = True

class MediaCreateDTO(BaseModel):
    stone_id: int
    url: str
    is_main_media: bool



# === DTO для создания камня ===
@dataclass
class StoneCreateDTO:
 
    title: str
    price: float
    description: Optional[str] = None
    color: Optional[str] = None
    user_id: Optional[int] = None
    add_media: Optional[List[str]] = None

    @classmethod
    def from_schema(cls, schema: "StoneCreate") -> "StoneCreateDTO":
        return cls(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            color=schema.color,
            user_id=schema.user_id,
            add_media=getattr(schema, 'add_media', None)
        )


# === DTO для обновления камня ===
@dataclass
class StoneUpdateDTO:
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    color: Optional[str] = None
    user_id: Optional[int] = None
    add_media: Optional[List[str]] = None

    @classmethod
    def from_schema(cls, schema: "StoneUpdate") -> "StoneUpdateDTO":
        return cls(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            color=schema.color,
            user_id=schema.user_id,
            add_media=getattr(schema, 'add_media', None)
        )


# === DTO для ответа ===
@dataclass
class StoneResponseDTO:
    id: int  
    title: str
    price: float
    description: Optional[str] = None
    color: Optional[str] = None
    user_id: Optional[int] = None
    add_media: Optional[List[str]] = None
   
    @classmethod
    def from_model(cls, model: "Stone") -> "StoneResponseDTO":
        return cls(
            id=model.id,
            title=model.title,
            description=model.description,
            price=float(model.price),  # Преобразуем Decimal в float
            color=model.color,
            user_id=model.user_id,
            add_media=getattr(model, 'add_media', None),
        )


# === DTO для списка камней ===
@dataclass
class StoneListDTO:
    items: List[StoneResponseDTO]
    total: int

@dataclass
class UserCreateDTO:
    username: str
    email: str
    password: str
    is_admin: bool = False

    @classmethod
    def from_schema(cls, schema):
        return cls(
            username=schema.username,
            email=schema.email,
            password=schema.password,
            is_admin=schema.is_admin
        )


@dataclass
class UserResponseDTO:
    id: int
    username: str
    email: str
    is_admin: bool

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            username=model.username,
            email=model.email,
            is_admin=model.is_admin
        )


@dataclass
class TokenDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass
class TokenPayloadDTO:
    sub: str
    username: str
    is_admin: bool
    exp: Optional[int] = None
    type: str = "access"