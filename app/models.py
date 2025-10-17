from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Education(BaseModel):
    """Education entry for resume"""
    institution: str = Field(..., description="Name of the educational institution")
    degree: str = Field(..., description="Degree or certification obtained")
    field_of_study: Optional[str] = Field(None, description="Field of study or major")
    start_date: Optional[str] = Field(None, description="Start date (e.g., '2018-09' or 'September 2018')")
    end_date: Optional[str] = Field(None, description="End date or 'Present' if ongoing")
    gpa: Optional[str] = Field(None, description="GPA or grade")
    achievements: Optional[List[str]] = Field(default_factory=list, description="Academic achievements")


class Experience(BaseModel):
    """Work experience entry for resume"""
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job title/position")
    location: Optional[str] = Field(None, description="Job location")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date or 'Present' if current")
    responsibilities: List[str] = Field(default_factory=list, description="Key responsibilities and achievements")


class Skill(BaseModel):
    """Skill entry for resume"""
    category: str = Field(..., description="Skill category (e.g., 'Programming Languages', 'Frameworks')")
    items: List[str] = Field(..., description="List of skills in this category")


class PersonalInfo(BaseModel):
    """Personal information for resume"""
    full_name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Current location (city, country)")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    website: Optional[str] = Field(None, description="Personal website URL")
    summary: Optional[str] = Field(None, description="Professional summary")


class ResumeData(BaseModel):
    """Complete resume data structure"""
    personal_info: PersonalInfo
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    certifications: Optional[List[str]] = Field(default_factory=list, description="Professional certifications")
    languages: Optional[List[str]] = Field(default_factory=list, description="Languages spoken")


class ResumeGenerationRequest(BaseModel):
    """Request to generate a resume"""
    resume_data: ResumeData
    target_role: Optional[str] = Field(None, description="Target job role/position")
    tone: Optional[str] = Field("professional", description="Tone of the resume (professional, creative, technical)")
    format_style: Optional[str] = Field("modern", description="Style of the resume (modern, classic, minimal)")


class ResumeGenerationResponse(BaseModel):
    """Response containing generated resume"""
    markdown_content: str = Field(..., description="Resume content in Markdown format")
    html_content: Optional[str] = Field(None, description="Resume content in HTML format")
    suggestions: Optional[List[str]] = Field(default_factory=list, description="AI suggestions for improvement")
