from datetime import datetime, timedelta, timezone  
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from passlib.context import CryptContext
from stone_site.core.config import settings
from stone_site.repositories.user_repository import UserRepository
from stone_site.repositories.dto import UserResponseDTO,TokenDTO,TokenPayloadDTO
from stone_site.schemas.auth import UserCreate


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
    pbkdf2_sha256__rounds=30000,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    # ==========================================
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

 
    # JWT токены 
    # ==========================================

    def create_access_token(self, user) -> str:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + expires_delta  
        payload = {
            "sub": str(user.id),
            "username": user.username,
            "is_admin": user.is_admin,
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def create_refresh_token(self, user) -> str:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        expire = datetime.now(timezone.utc) + expires_delta  

        payload = {
            "sub": str(user.id),
            "username": user.username,
            "is_admin": user.is_admin,
            "exp": expire,
            "type": "refresh"
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


    def decode_token(self, token: str) -> TokenPayloadDTO:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return TokenPayloadDTO(
                sub=payload.get("sub"),
                username=payload.get("username"),
                is_admin=payload.get("is_admin", False),
                exp=payload.get("exp"),
                type=payload.get("type", "access")
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )

    def decode_token_optional(self, token: str) -> Optional[TokenPayloadDTO]:
        try:
            return self.decode_token(token)
        except HTTPException:
            return None

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def register_user(self, user_data: UserCreate) -> UserResponseDTO:
        existing_user = await self.user_repo.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        existing_email = await self.user_repo.get_by_email(user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        hashed_password = self.get_password_hash(user_data.password)
        return await self.user_repo.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_admin=user_data.is_admin
        )

 
    async def login(self, username: str, password: str) -> TokenDTO:
        user = await self.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return TokenDTO(
            access_token=self.create_access_token(user),
            refresh_token=self.create_refresh_token(user)
        )

    async def refresh_token(self, refresh_token: str) -> TokenDTO:
        try:
            payload = self.decode_token(refresh_token)
            if payload.type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )

            user = await self.user_repo.get_model_by_id(int(payload.sub))
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )

            return TokenDTO(
                access_token=self.create_access_token(user),
                refresh_token=self.create_refresh_token(user)
            )
        except (JWTError, ValueError, HTTPException):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

  
    async def get_current_user(self, token: str) -> Optional[UserResponseDTO]:
        payload = self.decode_token_optional(token)
        if not payload:
            return None
        return await self.user_repo.get_by_id(int(payload.sub))

    async def get_current_user_model(self, token: str):
        payload = self.decode_token_optional(token)
        if not payload:
            return None
        return await self.user_repo.get_model_by_id(int(payload.sub))