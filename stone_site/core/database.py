from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from stone_site.core.config import settings
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

AsynсSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
async_session_maker = AsynсSessionLocal

async def get_db():
    """Dependency для получения сессии БД."""
    async with AsynсSessionLocal() as session:
        try:
            yield session
            await session.commit()  
        except Exception:
            await session.rollback()  
            raise
        finally:
            await session.close()  


class Base(DeclarativeBase):
    pass
