from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import resumes_router
from app.config import settings

# Create FastAPI application
app = FastAPI(
    title="AI Resume Builder API",
    description="FastAPI backend with AI integration for resume building and analysis",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resumes_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to AI Resume Builder API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
