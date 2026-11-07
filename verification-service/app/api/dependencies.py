import logging
from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.database.database import get_db_session
from app.services.verification_pipeline import VerificationPipeline

_pipeline: Optional[VerificationPipeline] = None


def get_app_settings() -> Settings:
    """Dependency for providing cached app settings."""
    return get_settings()


def get_app_logger() -> logging.Logger:
    """Dependency for providing logger instance."""
    return logging.getLogger("freshguard")


def get_pipeline(settings: Settings = Depends(get_app_settings)) -> VerificationPipeline:
    """Dependency provider for shared VerificationPipeline orchestrator."""
    global _pipeline
    if _pipeline is None:
        _pipeline = VerificationPipeline(settings=settings)
    return _pipeline
