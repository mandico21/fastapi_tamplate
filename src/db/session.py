from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import Settings, load_settings
from src.db.database import sa_sessionmaker


async def get_db_session() -> AsyncSession:
    settings: Settings = load_settings()
    session = sa_sessionmaker(settings.db)
    async with session() as session:
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
