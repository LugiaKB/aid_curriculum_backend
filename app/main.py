"""
FastAPI application factory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config.settings import settings
from app.api.router import api_router
from app.api.health import router as health_router


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        debug=settings.debug,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router, tags=["health"])
    app.include_router(api_router, prefix="/api/v1")
    
    return app


app = create_app()
