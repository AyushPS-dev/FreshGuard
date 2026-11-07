from functools import lru_cache
from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Core Application Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVICE_NAME: str = "freshguard-verification"
    VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"

    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./freshguard.db"

    # LLM Settings
    LLM_PROVIDER: str = "mock"  # "mock", "openai", "gemini"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_TIMEOUT_SECONDS: float = 15.0
    LLM_MAX_RETRIES: int = 2

    # Tavily API Settings
    TAVILY_API_KEY: str = Field(default="", validation_alias="TAVILY_API_KEY")
    TAVILY_TIMEOUT_SECONDS: float = Field(default=10.0, validation_alias="TAVILY_TIMEOUT")
    TAVILY_MAX_RETRIES: int = 2
    TAVILY_SEARCH_DEPTH: str = Field(default="advanced", validation_alias="TAVILY_SEARCH_DEPTH")
    TAVILY_MAX_RESULTS: int = Field(default=5, validation_alias="TAVILY_MAX_RESULTS")

    # Freshness Policy Default TTLs (in seconds, matching shared/contracts/README.md)
    TTL_SOFTWARE_VERSION: int = 86400   # 24 hours
    TTL_PRICING: int = 86400            # 24 hours
    TTL_LEADERSHIP: int = 604800        # 7 days
    TTL_BREAKING_NEWS: int = 300        # 5 minutes
    TTL_GENERAL: int = 43200            # 12 hours


@lru_cache
def get_settings() -> Settings:
    """Returns cached application settings instance."""
    return Settings()
