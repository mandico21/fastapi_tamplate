from typing import Callable

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings
from src.db.database import sa_sessionmaker


def stub():
    raise NotImplementedError


def db_session_provider(config: Settings) -> Callable[[], AsyncSession]:
    sessionmaker = sa_sessionmaker(config.db)

    async def get_db_session() -> AsyncSession:
        async with sessionmaker() as session:
            try:
                yield session
            except SQLAlchemyError as sql_ex:
                await session.rollback()
                raise sql_ex
            except HTTPException as http_ex:
                await session.rollback()
                raise http_ex
            finally:
                await session.close()

    return get_db_session
