"""FastAPI main application."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config import settings, init_sentry
from app.utils.errors import APIError
from app.api.v1 import health
from app.utils.logging import setup_structlog

# Setup logging
setup_structlog()
logger = structlog.get_logger(__name__)

# Initialize Sentry
init_sentry()

# Create FastAPI app
app = FastAPI(
    title="PaisaBuddy API",
    description="Monthly financial clarity for salaried Indians",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle API errors."""
    logger.warning(
        "api_error",
        code=exc.code.value,
        status=exc.status_code,
        user_facing=exc.user_facing,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": exc.code.value,
                "message": exc.message,
                "user_facing": exc.user_facing,
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception("unexpected_error", error=type(exc).__name__)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "E500",
                "message": "Something went wrong. Our team has been notified.",
                "user_facing": True,
            },
        },
    )


# Include routers
from app.api.v1 import auth, upload, reports
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(reports.router)


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "name": "PaisaBuddy API",
        "version": "0.1.0",
        "status": "running",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
