from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ResumeGenerationRequest, ResumeGenerationResponse
from app.services import ai_resume_service
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered resume building backend for Aid Curriculum"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=False,  # Disabled for security with wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Aid Curriculum Backend - Resume Builder API",
        "version": settings.app_version,
        "endpoints": {
            "health": "/health",
            "generate_resume": "/api/resume/generate (POST)",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "ai_enabled": settings.openai_api_key is not None
    }


@app.post("/api/resume/generate", response_model=ResumeGenerationResponse)
async def generate_resume(request: ResumeGenerationRequest):
    """
    Generate a resume using AI
    
    This endpoint takes structured resume data and generates a professional resume
    in Markdown format using AI. If AI is not available, it falls back to a basic template.
    
    Args:
        request: Resume generation request containing personal info, experience, education, skills, etc.
    
    Returns:
        ResumeGenerationResponse with the generated resume in Markdown format and suggestions
    """
    try:
        result = ai_resume_service.generate_resume(request)
        return ResumeGenerationResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate resume: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
