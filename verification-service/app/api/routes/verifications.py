from datetime import datetime, timezone
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_pipeline
from app.database.database import get_db_session
from app.database.models import VerificationRecord
from app.database.repository import VerificationRepository
from app.schemas.claims import ClaimVerdict, ClaimVerdictResult
from app.schemas.evidence import EvidenceMinimal, ensure_utc_datetime
from app.schemas.request import VerificationRequest
from app.schemas.response import VerificationResponse, VerificationStatus
from app.services.verification_pipeline import VerificationPipeline
from app.utils.exceptions import NotFoundError

logger = logging.getLogger("freshguard.api.verifications")

router = APIRouter(prefix="/v1/verifications", tags=["verifications"])


def record_to_response(record: VerificationRecord) -> VerificationResponse:
    """Converts a persisted VerificationRecord ORM instance into a VerificationResponse."""
    results: List[ClaimVerdictResult] = []
    for c in record.claims:
        ev_items = [
            EvidenceMinimal(title=ev.title, url=str(ev.url))
            for ev in c.evidence
        ]
        ev_ids = [ev.evidence_id for ev in c.evidence]
        results.append(
            ClaimVerdictResult(
                claim_id=c.claim_id,
                verdict=ClaimVerdict(c.verdict),
                confidence=c.confidence,
                reason=c.reason,
                evidence_ids=ev_ids,
                evidence=ev_items,
                corrected_value=c.corrected_value,
                checked_at=ensure_utc_datetime(c.checked_at),
            )
        )

    # Resolve status enum safely
    status_enum = (
        VerificationStatus(record.status)
        if record.status in [s.value for s in VerificationStatus]
        else VerificationStatus.COMPLETED
    )

    return VerificationResponse(
        request_id=record.request_id,
        verification_id=record.verification_id,
        status=status_enum,
        requires_refresh=record.requires_refresh,
        claims_checked=record.claims_checked,
        results=results,
        claims=results,
        processing_time_ms=record.processing_time_ms,
        checked_at=ensure_utc_datetime(record.checked_at),
    )


@router.post(
    "",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit LLM response text for freshness and factual verification",
)
@router.post(
    "/",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def create_verification(
    request: VerificationRequest,
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    pipeline: VerificationPipeline = Depends(get_pipeline),
    session: AsyncSession = Depends(get_db_session),
) -> VerificationResponse:
    """
    Evaluates response text against factual claims, real-time web evidence,
    and category-specific freshness policies.
    Provides idempotent deduplication when the same request_id is resubmitted.
    """
    if x_request_id and not request.request_id:
        request.request_id = x_request_id

    # Check for idempotency: existing verification for identical request_id
    existing_record = await VerificationRepository.get_verification_by_request_id(session, request.request_id)
    if existing_record is not None:
        logger.info("Idempotent hit: returning existing verification %s for request_id %s", existing_record.verification_id, request.request_id)
        return record_to_response(existing_record)

    try:
        logger.info("Starting verification for request %s (mode: %s)", request.request_id, request.mode)
        response = await pipeline.verify(request, session=session)
        return response
    except FreshGuardException:
        raise
    except Exception as exc:
        logger.error("Internal error during verification %s: %s", request.request_id, exc, exc_info=True)
        raise FreshGuardException(
            message="An internal server error occurred during verification.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="INTERNAL_SERVER_ERROR",
            details={},
        )


@router.get(
    "/{verification_id}",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a stored verification result by its unique verification ID",
)
async def get_verification(
    verification_id: str,
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
    session: AsyncSession = Depends(get_db_session),
) -> VerificationResponse:
    """
    Retrieves a historical verification record by verification ID.
    Returns HTTP 404 with standard APIError envelope if not found.
    """
    record = await VerificationRepository.get_verification_by_id(session, verification_id)
    if not record:
        logger.warning("Verification with ID '%s' not found (request_id=%s)", verification_id, x_request_id)
        raise NotFoundError(
            message=f"Verification with ID '{verification_id}' was not found.",
            details={"verification_id": verification_id, "request_id": x_request_id},
        )

    return record_to_response(record)
