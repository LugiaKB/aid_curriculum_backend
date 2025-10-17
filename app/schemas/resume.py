from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date


class ContactInfo(BaseModel):
    """Contact information schema."""
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class Education(BaseModel):
    """Education entry schema."""
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    description: Optional[str] = None


class Experience(BaseModel):
    """Work experience entry schema."""
    company: str
    position: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    description: Optional[str] = None
    achievements: Optional[List[str]] = []


class Project(BaseModel):
    """Project entry schema."""
    name: str
    description: str
    technologies: Optional[List[str]] = []
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Skill(BaseModel):
    """Skill entry schema."""
    category: str
    skills: List[str]


class ResumeCreate(BaseModel):
    """Schema for creating a new resume."""
    full_name: str
    professional_title: Optional[str] = None
    summary: Optional[str] = None
    contact: ContactInfo
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[Project] = []
    skills: List[Skill] = []


class ResumeResponse(ResumeCreate):
    """Schema for resume response."""
    id: str
    
    class Config:
        from_attributes = True


class ResumeGenerateRequest(BaseModel):
    """Schema for AI resume generation request."""
    job_description: str
    user_info: Optional[str] = Field(
        None, 
        description="Additional user information or existing resume content"
    )
    experience_level: Optional[str] = Field(
        "mid-level", 
        description="Career level: entry-level, mid-level, senior, expert"
    )
    include_sections: Optional[List[str]] = Field(
        default_factory=lambda: ["summary", "skills", "experience", "projects"],
        description="Sections to include in the generated resume"
    )


class ResumeGenerateResponse(BaseModel):
    """Schema for AI resume generation response."""
    generated_content: dict
    suggestions: Optional[List[str]] = []
    

class ResumeAnalysisRequest(BaseModel):
    """Schema for resume analysis request."""
    resume_content: str
    job_description: Optional[str] = None


class ResumeAnalysisResponse(BaseModel):
    """Schema for resume analysis response."""
    score: float = Field(..., ge=0, le=100, description="Overall resume score")
    strengths: List[str]
    improvements: List[str]
    keywords_match: Optional[dict] = None
    suggestions: List[str]
