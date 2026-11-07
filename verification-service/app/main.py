from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health
from app.config import get_settings
from app.utils.exceptions import FreshGuardException
from app.utils.logging import logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    settings = get_settings()
    setup_logging(log_level=settings.LOG_LEVEL)
    logger.info(
        "Starting %s (v%s) in %s mode",
        settings.SERVICE_NAME,
        settings.VERSION,
        settings.ENVIRONMENT,
    )
    yield
    logger.info("Shutting down %s", settings.SERVICE_NAME)


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="FreshGuard Verification Service",
        description="Real-time freshness verification and semantic cache protection layer for LLMs.",
        version=settings.VERSION,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Centralized Exception Handlers
    @app.exception_handler(FreshGuardException)
    async def freshguard_exception_handler(request: Request, exc: FreshGuardException) -> JSONResponse:
        logger.warning(
            "FreshGuardException: %s [%s] Path: %s Details: %s",
            exc.message,
            exc.code,
            request.url.path,
            exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "code": exc.code,
                "details": exc.details,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning("Validation error on path %s: %s", request.url.path, exc.errors())
        return JSONResponse(
            status_code=422,
            content={
                "error": "Request validation failed.",
                "code": "VALIDATION_ERROR",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unhandled exception on %s: %s",
            request.url.path,
            str(exc),
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "An internal server error occurred.",
                "code": "INTERNAL_SERVER_ERROR",
                "details": {},
            },
        )

    # Register Routers
    app.include_router(health.router)

    return app


app = create_app()
