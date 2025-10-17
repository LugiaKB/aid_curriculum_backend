"""
Main application entry point
Run with: python main.py
Or with uvicorn: uvicorn app.main:app --reload
"""

import uvicorn
from app import __version__
from app.config.settings import settings


def main():
    """
    Main function to start the application
    """
    print(f"Aid Curriculum Backend v{__version__}")
    print(f"Starting server on {settings.host}:{settings.port}...")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
