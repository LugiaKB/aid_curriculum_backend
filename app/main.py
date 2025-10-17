from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.models import ResumeData, ResumeResponse
from typing import Dict
import uuid

app = FastAPI(
    title="AID Curriculum Backend",
    description="API for building and managing resumes",
    version="1.0.0"
)

# Configure CORS
# Note: In production, replace allow_origins=["*"] with specific origins
# Using "*" with allow_credentials=True is a security risk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for resumes (no database for now)
resumes_store: Dict[str, ResumeData] = {}


@app.get("/")
async def root():
    """Root endpoint"""
    # Note: This endpoints list is hardcoded. For a dynamic list, use app.routes
    return {
        "message": "Welcome to AID Curriculum Backend API",
        "version": "1.0.0",
        "endpoints": {
            "POST /resume": "Create a new resume",
            "GET /resume/{resume_id}": "Get a resume by ID",
            "PUT /resume/{resume_id}": "Update a resume by ID",
            "DELETE /resume/{resume_id}": "Delete a resume by ID"
        }
    }


@app.post("/resume", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(resume_data: ResumeData):
    """
    Create a new resume with the provided data.
    
    Returns the created resume with a unique ID.
    """
    # Generate a unique ID for the resume
    resume_id = str(uuid.uuid4())
    
    # Store the resume in memory
    resumes_store[resume_id] = resume_data
    
    return ResumeResponse(
        status="success",
        message=f"Resume created successfully with ID: {resume_id}",
        resume_id=resume_id,
        data=resume_data
    )


@app.get("/resume/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str):
    """
    Retrieve a resume by its ID.
    
    Returns the resume data if found.
    """
    if resume_id not in resumes_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    
    resume_data = resumes_store[resume_id]
    
    return ResumeResponse(
        status="success",
        message="Resume retrieved successfully",
        resume_id=resume_id,
        data=resume_data
    )


@app.put("/resume/{resume_id}", response_model=ResumeResponse)
async def update_resume(resume_id: str, resume_data: ResumeData):
    """
    Update an existing resume by its ID.
    
    Returns the updated resume data.
    """
    if resume_id not in resumes_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    
    # Update the resume
    resumes_store[resume_id] = resume_data
    
    return ResumeResponse(
        status="success",
        message="Resume updated successfully",
        resume_id=resume_id,
        data=resume_data
    )


@app.delete("/resume/{resume_id}")
async def delete_resume(resume_id: str):
    """
    Delete a resume by its ID.
    
    Returns a confirmation message.
    """
    if resume_id not in resumes_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found"
        )
    
    # Delete the resume
    del resumes_store[resume_id]
    
    return {
        "status": "success",
        "message": f"Resume with ID {resume_id} deleted successfully"
    }


@app.get("/resumes")
async def list_resumes():
    """
    List all stored resumes (returns resume IDs only).
    
    This is useful for checking which resumes are currently stored in memory.
    """
    return {
        "status": "success",
        "count": len(resumes_store),
        "resume_ids": list(resumes_store.keys())
    }
