from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.schemas.evidence import EvidenceItem, EvidenceMinimal, ensure_utc_datetime


class ClaimCategory(str, Enum):
    """Categories of claims verified by FreshGuard."""
    SOFTWARE_VERSION = "software_version"
    PRICING = "pricing"
    LEADERSHIP = "leadership"
    PRODUCT_AVAILABILITY = "product_availability"
    RECENT_EVENTS = "recent_events"
    TECHNOLOGY_RELEASES = "technology_releases"
    CURRENT_STATISTICS = "current_statistics"
    GENERAL_KNOWLEDGE = "general_knowledge"
    OTHER = "other"


class ClaimVerdict(str, Enum):
    """Verification verdict for an individual factual claim."""
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNCLEAR = "UNCLEAR"

    @classmethod
    def _missing_(cls, value: object):
        """Allow case-insensitive resolution (e.g. 'supported' -> SUPPORTED)."""
        if isinstance(value, str):
            for member in cls:
                if member.value.upper() == value.upper():
                    return member
        return None


class ExtractedClaim(BaseModel):
    """Represents a discrete, structured factual claim extracted from an LLM response."""
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    claim_id: str = Field(..., min_length=1, max_length=128, description="Deterministic identifier for the claim")
    text: str = Field(..., min_length=1, max_length=2000, alias="original_text", description="Verbatim or summarized statement")
    category: ClaimCategory = Field(default=ClaimCategory.OTHER, description="Category classification")
    entity: str = Field(..., min_length=1, max_length=256, description="Subject entity (e.g., Python, Stripe, OpenAI)")
    attribute: str = Field(..., min_length=1, max_length=256, description="Attribute of subject (e.g., latest_version, pro_price, ceo)")
    time_sensitive: bool = Field(default=True, description="Whether this claim is subject to change over time")

    @field_validator("category", mode="before")
    @classmethod
    def parse_category(cls, v: Union[str, ClaimCategory]) -> ClaimCategory:
        if isinstance(v, ClaimCategory):
            return v
        if isinstance(v, str):
            normalized = v.strip().lower().replace(" ", "_").replace("-", "_")
            for member in ClaimCategory:
                if member.value == normalized:
                    return member
        return ClaimCategory.OTHER


class ClaimExtractionRequest(BaseModel):
    """Input payload to trigger structured claim extraction."""
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    text: str = Field(..., min_length=1, max_length=50000, alias="response_text", description="LLM text to extract claims from")


class ClaimExtractionResponse(BaseModel):
    """Output payload from structured claim extraction."""
    model_config = ConfigDict(populate_by_name=True)

    claims: List[ExtractedClaim] = Field(default_factory=list, description="List of extracted factual claims")


class ClaimVerdictResult(BaseModel):
    """Verification judgment on an individual extracted claim."""
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    claim_id: str = Field(..., min_length=1, max_length=128, description="Identifier of the claim verified")
    verdict: ClaimVerdict = Field(..., description="Verdict outcome: SUPPORTED, CONTRADICTED, or UNCLEAR")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score calibrated between 0.0 and 1.0")
    reason: str = Field(..., min_length=1, max_length=2000, description="Justification grounded strictly in evidence")
    evidence_ids: List[str] = Field(default_factory=list, description="List of evidence IDs grounding this verdict")
    evidence: List[Union[EvidenceItem, EvidenceMinimal]] = Field(default_factory=list, description="Evidence items attached to this claim")
    corrected_value: Optional[str] = Field(default=None, description="Correct value if claim was contradicted")
    checked_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Verification check timestamp in UTC",
    )

    @field_validator("checked_at", mode="after")
    @classmethod
    def validate_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        return ensure_utc_datetime(v)

    @field_validator("verdict", mode="before")
    @classmethod
    def parse_verdict(cls, v: Union[str, ClaimVerdict]) -> ClaimVerdict:
        if isinstance(v, ClaimVerdict):
            return v
        if isinstance(v, str):
            res = ClaimVerdict._missing_(v)
            if res is not None:
                return res
        raise ValueError(f"Invalid verdict: {v}. Must be SUPPORTED, CONTRADICTED, or UNCLEAR.")
