from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.schemas.claims import ClaimVerdictResult
from app.schemas.evidence import ensure_utc_datetime


class VerificationStatus(str, Enum):
    """Overall status of a verification request."""
    # Semantic Freshness Statuses
    FRESH = "FRESH"
    STALE = "STALE"
    UNCERTAIN = "UNCERTAIN"
    NOT_REQUIRED = "NOT_REQUIRED"

    # Gateway Lifecycle Statuses (Go contract compatibility)
    ACCEPTED = "accepted"
    COMPLETED = "completed"
    FAILED = "failed"

    @classmethod
    def _missing_(cls, value: object):
        """Allow case-insensitive lookup."""
        if isinstance(value, str):
            for member in cls:
                if member.value.upper() == value.upper():
                    return member
        return None


class APIErrorDetail(BaseModel):
    """Cross-service machine-readable error payload matching shared contracts."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable description of the error")
    request_id: str = Field(..., description="Correlation ID for the failed request")
    retryable: bool = Field(default=False, description="Whether caller may safely retry")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Optional structured debug context")


class VerificationResponse(BaseModel):
    """
    Standard verification response payload.
    Compatible with Go Bifrost gateway adapter, Next.js frontend, and evaluation harnesses.
    """
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    request_id: str = Field(..., min_length=1, max_length=128, description="Correlation identifier matching request")
    verification_id: Optional[str] = Field(default=None, description="Unique verification job identifier")
    status: VerificationStatus = Field(..., description="FRESH, STALE, UNCERTAIN, or NOT_REQUIRED")
    requires_refresh: bool = Field(..., description="Whether cached response should be invalidated/refreshed")
    claims_checked: int = Field(default=0, ge=0, description="Count of time-sensitive claims evaluated")
    results: List[ClaimVerdictResult] = Field(default_factory=list, description="Detailed verification results per claim")
    claims: Optional[List[ClaimVerdictResult]] = Field(
        default=None,
        description="Alias for results matching shared/schemas/verification_api.json",
    )
    processing_time_ms: int = Field(default=0, ge=0, description="Verification latency in milliseconds")
    checked_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of completion in UTC",
    )
    result_url: Optional[str] = Field(default=None, description="Result retrieval URL for async workflows")
    error: Optional[APIErrorDetail] = Field(default=None, description="Error detail if status is failed")

    @field_validator("checked_at", mode="after")
    @classmethod
    def validate_utc(cls, v: Optional[datetime]) -> Optional[datetime]:
        return ensure_utc_datetime(v)

    @field_validator("status", mode="before")
    @classmethod
    def parse_status(cls, v: Union[str, VerificationStatus]) -> VerificationStatus:
        if isinstance(v, VerificationStatus):
            return v
        if isinstance(v, str):
            res = VerificationStatus._missing_(v)
            if res is not None:
                return res
        raise ValueError(f"Invalid status: {v}. Must be a valid VerificationStatus enum value.")

    @model_validator(mode="after")
    def sync_claims_and_results(self) -> "VerificationResponse":
        """Ensures results and claims mirror each other for full Go/TS compatibility."""
        if not self.claims and self.results:
            self.claims = self.results
        elif not self.results and self.claims:
            self.results = self.claims
            self.claims_checked = len(self.claims)
        return self
