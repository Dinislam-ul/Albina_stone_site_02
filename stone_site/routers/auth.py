from fastapi import APIRouter, Depends, status
from stone_site.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from stone_site.service.auth_service import AuthService
from stone_site.schemas.auth import UserResponse, Token, LoginRequest, RefreshTokenRequest, UserCreate

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate,db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.register_user(user_data)


@auth_router.post("/login", response_model=Token)
async def login(login_data: LoginRequest,db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.login(login_data.username, login_data.password)


@auth_router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest,db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    return await auth_service.refresh_token(refresh_data.refresh_token)

