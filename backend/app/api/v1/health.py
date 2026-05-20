"""Health check endpoint."""
from fastapi import APIRouter

from app.config import settings
from app.api.schemas import APIResponse, HealthResponse

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT,
    )
