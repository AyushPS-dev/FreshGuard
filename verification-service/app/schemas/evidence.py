from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class EvidenceSourceType(str, Enum):
    """Source classification for retrieved web evidence."""
    OFFICIAL_DOCS = "official_docs"
    NEWS = "news"
    WEBSITE = "website"
    OTHER = "other"


def ensure_utc_datetime(v: Optional[datetime]) -> Optional[datetime]:
    """Ensures datetime is timezone-aware and set to UTC."""
    if v is None:
        return None
    if v.tzinfo is None:
        return v.replace(tzinfo=timezone.utc)
    return v.astimezone(timezone.utc)


class EvidenceItem(BaseModel):
    """Normalized evidence item attached to claim verdicts."""
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    evidence_id: Optional[str] = Field(default=None, description="Unique identifier for the evidence snippet")
    title: str = Field(..., min_length=1, max_length=500, alias="source_title", description="Title of the source webpage")
    url: HttpUrl = Field(..., alias="source_url", description="Verified source URL")
    content: Optional[str] = Field(default="", max_length=10000, alias="snippet", description="Extracted textual content or snippet")
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence/relevance score between 0.0 and 1.0")
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Time the evidence was retrieved in UTC",
    )
    published_at: Optional[datetime] = Field(default=None, description="Original publication timestamp if available")
    source_type: EvidenceSourceType = Field(default=EvidenceSourceType.WEBSITE, description="Type of evidence source")

    @field_validator("retrieved_at", "published_at", mode="after")
    @classmethod
    def validate_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        return ensure_utc_datetime(v)

    def model_dump(self, *args, **kwargs):
        """Custom dump ensuring HttpUrl is serialized to string."""
        d = super().model_dump(*args, **kwargs)
        if "url" in d and d["url"] is not None:
            d["url"] = str(d["url"])
        if "source_url" in d and d["source_url"] is not None:
            d["source_url"] = str(d["source_url"])
        return d


class EvidenceMinimal(BaseModel):
    """Minimal evidence format for concise API responses."""
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    title: str = Field(..., min_length=1, max_length=500, alias="source_title")
    url: str = Field(..., alias="source_url")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        # Validate that string starts with http:// or https://
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v
