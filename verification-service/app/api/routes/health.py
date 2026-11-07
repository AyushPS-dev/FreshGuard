from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.dependencies import get_app_settings
from app.config import Settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@router.get("/health", response_model=HealthResponse, summary="Service Health Check")
async def health_check(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    """
    Returns the health status, service identifier, and version of FreshGuard.
    """
    return HealthResponse(
        status="healthy",
        service=settings.SERVICE_NAME,
        version=settings.VERSION,
    )
