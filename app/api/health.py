"""
Health check endpoint
"""

from fastapi import APIRouter
from app import __version__

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": __version__
    }
