from typing import List, Optional
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)
import re


class CVRequest(BaseModel):
    full_name: str = Field(..., min_length=3, description="Nome completo do usuário")

    desired_role: str = Field(
        ..., min_length=2, description="Título profissional que está buscando"
    )

    email: Optional[EmailStr] = Field(None, description="Endereço de email válido")

    phone: Optional[str] = Field(None, description="Número de telefone com DDD")

    professional_experience: str = Field(
        ..., min_length=10, description="Descrição livre das experiências profissionais"
    )

    education: str = Field(
        ..., min_length=10, description="Descrição livre da formação acadêmica"
    )

    skills: str = Field(
        ..., min_length=5, description="Descrição livre das habilidades e competências"
    )

    target_job_description: Optional[str] = Field(
        None, description="Descrição da vaga alvo (opcional)"
    )

    @field_validator("phone")
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove todos os caracteres não numéricos
        numbers_only = re.sub(r"\D", "", v)
        # Verifica se o número tem entre 10 e 11 dígitos (com ou sem 9)
        if not (10 <= len(numbers_only) <= 11):
            raise ValueError("Número de telefone deve ter 10 ou 11 dígitos")
        return numbers_only

    @field_validator("full_name")
    def validate_name(cls, v):
        if len(v.split()) < 2:
            raise ValueError("Por favor, forneça nome e sobrenome")
        return v.title()  # Capitaliza as primeiras letras

    @model_validator(mode="before")
    def validate_contact(cls, data):
        if isinstance(data, dict):
            email = data.get("email")
            phone = data.get("phone")
            if not email and not phone:
                raise ValueError(
                    "Pelo menos um meio de contato (email ou telefone) deve ser fornecido"
                )
        return data


class LearningResource(BaseModel):
    title: str
    url: str
    type: str  # e.g., "course", "tutorial", "documentation"
    platform: str  # e.g., "Coursera", "Udemy", "YouTube"
    description: str

    model_config = {"extra": "forbid"}


class SkillAnalysis(BaseModel):
    skill_name: str
    required_by_job: bool
    user_has_skill: bool
    proficiency_level: Optional[str] = None  # e.g., "basic", "intermediate", "advanced"
    gap_description: Optional[str] = None


class SkillStatus(BaseModel):
    name: str
    has_skill: bool

    model_config = {"extra": "forbid"}


class JobCompatibilityAnalysis(BaseModel):
    compatibility_score: float = Field(..., ge=0, le=100)  # percentage
    skills: List[SkillStatus]  # Lista de todas as skills com seu status
    improvement_suggestions: List[str]
    learning_resources: List[LearningResource]

    model_config = {"extra": "forbid"}


class PersonalInfo(BaseModel):
    name: str
    title: str
    email: Optional[str] = None
    phone: Optional[str] = None

    model_config = {"extra": "forbid"}


class ExperienceEntry(BaseModel):
    title: str
    company: str
    period: str
    achievements: List[str]

    model_config = {"extra": "forbid"}


class EducationEntry(BaseModel):
    degree: str
    institution: str
    period: str

    model_config = {"extra": "forbid"}


class Language(BaseModel):
    name: str
    level: str

    model_config = {"extra": "forbid"}


class GeneratedCV(BaseModel):
    personal_info: PersonalInfo
    professional_summary: str
    experience_entries: List[ExperienceEntry]
    education_entries: List[EducationEntry]
    skills: List[str]
    achievements: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    languages: Optional[List[Language]] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "personal_info": {
                    "name": "Maria Silva",
                    "title": "Desenvolvedora Full Stack Senior",
                    "email": "maria@email.com",
                    "phone": "11987654321",
                },
                "professional_summary": "Desenvolvedora Full Stack com 5 anos...",
                "experience_entries": [
                    {
                        "title": "Desenvolvedora Full Stack Senior",
                        "company": "TechBR",
                        "period": "2022 - Presente",
                        "achievements": [
                            "Liderou equipe de 5 desenvolvedores...",
                            "Implementou CI/CD pipeline...",
                        ],
                    }
                ],
                "education_entries": [
                    {
                        "degree": "Bacharel em Ciência da Computação",
                        "institution": "UFMG",
                        "period": "2017 - 2021",
                    }
                ],
                "skills": [
                    "Python (Avançado)",
                    "React (Intermediário)",
                    "AWS (Básico)",
                ],
            }
        },
    }


class CVResponse(BaseModel):
    generated_cv: GeneratedCV
    job_compatibility: Optional[JobCompatibilityAnalysis] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "generated_cv": {
                    "personal_info": {
                        "name": "Maria Silva",
                        "title": "Desenvolvedora Full Stack Senior",
                        "email": "maria@email.com",
                        "phone": "11987654321",
                    },
                    "professional_summary": "Desenvolvedora Full Stack com 5 anos...",
                    "experience_entries": [
                        {
                            "title": "Desenvolvedora Full Stack Senior",
                            "company": "TechBR",
                            "period": "2022 - Presente",
                            "achievements": [
                                "Liderou equipe de 5 desenvolvedores...",
                                "Implementou CI/CD pipeline...",
                            ],
                        }
                    ],
                    "education_entries": [
                        {
                            "degree": "Bacharel em Ciência da Computação",
                            "institution": "UFMG",
                            "period": "2017 - 2021",
                        }
                    ],
                    "skills": [
                        "Python (Avançado)",
                        "React (Intermediário)",
                        "AWS (Básico)",
                    ],
                },
                "job_compatibility": {
                    "compatibility_score": 85.5,
                    "skills": [
                        {"name": "Python", "has_skill": True},
                        {"name": "React", "has_skill": True},
                        {"name": "Kubernetes", "has_skill": False},
                    ],
                    "improvement_suggestions": [
                        "Considere aprofundar seus conhecimentos em containers com Kubernetes",
                        "Aprenda GraphQL para complementar suas habilidades em APIs",
                    ],
                    "learning_resources": [
                        {
                            "title": "Kubernetes for Developers",
                            "url": "https://example.com/course",
                            "type": "course",
                            "platform": "Udemy",
                            "description": "Curso completo de Kubernetes...",
                        }
                    ],
                },
            }
        },
    }
