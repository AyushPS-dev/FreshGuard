from collections.abc import AsyncGenerator
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings
from app.database.models import Base

logger = logging.getLogger("freshguard.database")

_engine: Optional[AsyncEngine] = None
_sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine(database_url: Optional[str] = None) -> AsyncEngine:
    """Returns or initializes the singleton AsyncEngine."""
    global _engine
    if _engine is None:
        url = database_url or get_settings().DATABASE_URL
        # SQLite async connection setup
        connect_args = {"check_same_thread": False} if "sqlite" in url else {}
        _engine = create_async_engine(
            url,
            echo=False,
            future=True,
            connect_args=connect_args,
        )
        logger.info("Initialized async database engine with URL: %s", url)
    return _engine


def get_sessionmaker(engine: Optional[AsyncEngine] = None) -> async_sessionmaker[AsyncSession]:
    """Returns or initializes the singleton async_sessionmaker."""
    global _sessionmaker
    if _sessionmaker is None:
        eng = engine or get_engine()
        _sessionmaker = async_sessionmaker(
            bind=eng,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return _sessionmaker


async def init_db(engine: Optional[AsyncEngine] = None) -> None:
    """Initializes tables in database schema."""
    eng = engine or get_engine()
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables verified and initialized.")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for scoped transactional database sessions."""
    sm = get_sessionmaker()
    async with sm() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
