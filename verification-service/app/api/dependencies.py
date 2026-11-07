import logging
from app.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Dependency for providing cached app settings."""
    return get_settings()


def get_app_logger() -> logging.Logger:
    """Dependency for providing logger instance."""
    return logging.getLogger("freshguard")
