from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date


class Education(BaseModel):
    """Education entry for resume"""
    institution: str = Field(..., description="Name of educational institution")
    degree: str = Field(..., description="Degree or certification obtained")
    field_of_study: Optional[str] = Field(None, description="Field of study")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date or expected graduation")
    gpa: Optional[str] = Field(None, description="GPA or grade")
    description: Optional[str] = Field(None, description="Additional details")


class Experience(BaseModel):
    """Work experience entry for resume"""
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job title/position")
    location: Optional[str] = Field(None, description="Location of job")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date (null if current)")
    description: Optional[str] = Field(None, description="Job responsibilities and achievements")
    is_current: bool = Field(False, description="Whether this is current position")


class Project(BaseModel):
    """Project entry for resume"""
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    technologies: Optional[List[str]] = Field(None, description="Technologies used")
    url: Optional[str] = Field(None, description="Project URL")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date")


class Certification(BaseModel):
    """Certification entry for resume"""
    name: str = Field(..., description="Certification name")
    issuer: str = Field(..., description="Issuing organization")
    date_obtained: Optional[date] = Field(None, description="Date obtained")
    expiry_date: Optional[date] = Field(None, description="Expiry date if applicable")
    credential_id: Optional[str] = Field(None, description="Credential ID")


class ResumeData(BaseModel):
    """Complete resume data structure"""
    # Personal Information
    full_name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City, State/Country")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    website: Optional[str] = Field(None, description="Personal website URL")
    
    # Summary
    summary: Optional[str] = Field(None, description="Professional summary or objective")
    
    # Skills
    skills: Optional[List[str]] = Field(None, description="List of skills")
    
    # Experience
    experience: Optional[List[Experience]] = Field(None, description="Work experience entries")
    
    # Education
    education: Optional[List[Education]] = Field(None, description="Education entries")
    
    # Projects
    projects: Optional[List[Project]] = Field(None, description="Project entries")
    
    # Certifications
    certifications: Optional[List[Certification]] = Field(None, description="Certification entries")
    
    # Additional sections
    languages: Optional[List[str]] = Field(None, description="Languages spoken")
    interests: Optional[List[str]] = Field(None, description="Interests and hobbies")


class ResumeResponse(BaseModel):
    """Response model for resume endpoints"""
    status: str = Field(..., description="Status of the request")
    message: str = Field(..., description="Response message")
    resume_id: Optional[str] = Field(None, description="Resume ID")
    data: ResumeData = Field(..., description="Resume data")
