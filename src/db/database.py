import sqlalchemy as sa
from sqlalchemy import DateTime, Column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import DB


def make_connection_string(db: DB, async_fallback: bool = False) -> str:
    result = (
        f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"
    )
    if async_fallback:
        result += "?async_fallback=True"
    return result


def sa_sessionmaker(db: DB, echo: bool = False) -> sessionmaker:
    engine = create_async_engine(make_connection_string(db), echo=echo)
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True,
        autoflush=False,
    )


Base = declarative_base()


class TimedBaseModel(Base):
    """Основная модель с датой"""

    __abstract__ = True

    created_at = Column(DateTime(True), server_default=sa.func.now())
    updated_at = Column(DateTime(True), default=sa.func.now(), onupdate=sa.func.now(),
                        server_default=sa.func.now())
