from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas import (
    ResumeCreate,
    ResumeResponse,
    ResumeGenerateRequest,
    ResumeGenerateResponse,
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
)
from app.models import resume_model
from app.services import ai_service

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(resume: ResumeCreate):
    """Create a new resume."""
    resume_data = resume.model_dump()
    created_resume = resume_model.create(resume_data)
    return created_resume


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes():
    """List all resumes."""
    resumes = resume_model.get_all()
    return resumes


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str):
    """Get a specific resume by ID."""
    resume = resume_model.get(resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(resume_id: str, resume: ResumeCreate):
    """Update an existing resume."""
    resume_data = resume.model_dump()
    updated_resume = resume_model.update(resume_id, resume_data)
    if not updated_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )
    return updated_resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: str):
    """Delete a resume."""
    deleted = resume_model.delete(resume_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )
    return None


@router.post("/generate", response_model=ResumeGenerateResponse)
async def generate_resume(request: ResumeGenerateRequest):
    """
    Generate resume content using AI based on job description.
    
    This endpoint uses AI to generate tailored resume content including:
    - Professional summary
    - Relevant skills
    - Experience suggestions
    - Project ideas
    """
    try:
        generated_content = await ai_service.generate_resume_content(
            job_description=request.job_description,
            user_info=request.user_info,
            experience_level=request.experience_level,
            include_sections=request.include_sections
        )
        
        suggestions = [
            "Review and customize the generated content to match your experience",
            "Add specific metrics and achievements",
            "Ensure all information is accurate and truthful",
            "Tailor the content for each job application"
        ]
        
        return ResumeGenerateResponse(
            generated_content=generated_content,
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating resume content: {str(e)}"
        )


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze resume content and provide feedback.
    
    This endpoint uses AI to analyze a resume and provide:
    - Overall score (0-100)
    - Strengths
    - Areas for improvement
    - Keyword matching (if job description provided)
    - Actionable suggestions
    """
    try:
        analysis = await ai_service.analyze_resume(
            resume_content=request.resume_content,
            job_description=request.job_description
        )
        
        return ResumeAnalysisResponse(
            score=analysis.get("score", 70.0),
            strengths=analysis.get("strengths", []),
            improvements=analysis.get("improvements", []),
            keywords_match=analysis.get("keywords_match"),
            suggestions=analysis.get("suggestions", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resume: {str(e)}"
        )
