from sqlalchemy.orm import Mapped, mapped_column, relationship
from stone_site.core.database import Base
from sqlalchemy import String, Numeric, ForeignKey, Boolean
from typing import List, Optional


class Base(Base):
    __abstract__=True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    stones: Mapped[List["Stone"]] = relationship("Stone",back_populates="owner",cascade="all, delete-orphan")


class Stone(Base):
    __tablename__="stones"

    title: Mapped[str] = mapped_column(String(50), default="Stone")
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    color: Mapped[str]

    media: Mapped[List["Media"]] = relationship("Media",back_populates="stone", cascade="all, delete-orphan")
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"),nullable=True,index=True)
    owner: Mapped[Optional["User"]] = relationship("User",back_populates="stones")


class Media(Base):
    __tablename__="media"
    
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_main_media: Mapped[bool] = mapped_column(default=False)

    stone_id: Mapped[int] = mapped_column(ForeignKey("stones.id", ondelete="CASCADE"), nullable=False)
    stone: Mapped["Stone"]= relationship("Stone", back_populates="media")

