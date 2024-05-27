from sqlalchemy import DateTime, func, BigInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    premium: Mapped[bool] = mapped_column(Boolean, default=False)


class TypeEvent(Base):
    __tablename__ = 'type_event'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title = Mapped[str] = mapped_column(String(150), nullable=True)


class Event(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    type_event_id = Mapped
    title: Mapped[str] = mapped_column(String(150), nullable=True)
    url: Mapped[str] = mapped_column(String(130), nullable=True)


class Winner(Base):
    __tablename__ = 'winner'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id', ondelete='CASCADE'), nullable=False)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


class Settings(Base):
    __tablename__ = 'settings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    on_complex: Mapped[bool] = mapped_column(Boolean, nullable=False)
    on_place: Mapped[bool] = mapped_column(Boolean, nullable=False)
