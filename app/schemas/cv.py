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
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        
        # Remove todos os caracteres não numéricos
        numbers_only = re.sub(r"\D", "", v)
        
        # Verifica se o número tem entre 10 e 11 dígitos (com ou sem 9)
        if not (10 <= len(numbers_only) <= 11):
            raise ValueError(
                "Número de telefone deve ter 10 ou 11 dígitos. "
                "Exemplos válidos: (11) 99999-9999, 11999999999, 1199999999"
            )
        
        # Verifica se não é uma sequência repetitiva óbvia
        if len(set(numbers_only)) <= 2:
            raise ValueError(
                "Número de telefone parece inválido. "
                "Por favor, forneça um número de telefone real."
            )
            
        return numbers_only

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Nome não pode estar vazio")
        
        # Remove espaços extras e verifica se tem pelo menos 2 palavras
        clean_name = " ".join(v.strip().split())
        if len(clean_name.split()) < 2:
            raise ValueError(
                "Por favor, forneça nome e sobrenome completos. "
                "Exemplo: 'Maria Silva Santos'"
            )
        
        # Verifica se não contém números ou caracteres especiais
        if re.search(r'[0-9@#$%^&*()_+=\[\]{};:"\\|,.<>?/]', clean_name):
            raise ValueError(
                "Nome deve conter apenas letras e espaços. "
                "Não são permitidos números ou símbolos."
            )
            
        return clean_name.title()  # Capitaliza as primeiras letras

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v):
        if v is None:
            return v
        
        # Validação adicional para emails
        email_str = str(v).lower().strip()
        
        # Verifica domínios suspeitos ou muito simples
        common_invalid_domains = ['test.com', 'example.com', 'temp.com', 'fake.com']
        domain = email_str.split('@')[-1] if '@' in email_str else ''
        
        if domain in common_invalid_domains:
            raise ValueError(
                "Por favor, forneça um endereço de email real e válido. "
                f"O domínio '{domain}' não é aceito."
            )
            
        return email_str

    @field_validator("desired_role")
    @classmethod
    def validate_desired_role(cls, v):
        if not v or not v.strip():
            raise ValueError("Cargo desejado não pode estar vazio")
        
        clean_role = v.strip()
        if len(clean_role) < 3:
            raise ValueError(
                "Cargo desejado deve ter pelo menos 3 caracteres. "
                "Exemplo: 'Desenvolvedor Python', 'Analista de Dados'"
            )
            
        return clean_role.title()

    @field_validator("professional_experience")
    @classmethod
    def validate_professional_experience(cls, v):
        if not v or not v.strip():
            raise ValueError("Experiência profissional não pode estar vazia")
        
        clean_exp = v.strip()
        if len(clean_exp) < 20:
            raise ValueError(
                "Experiência profissional deve ser mais detalhada. "
                "Inclua informações sobre suas funções, projetos e conquistas (mínimo 20 caracteres)."
            )
            
        return clean_exp

    @field_validator("education")
    @classmethod
    def validate_education(cls, v):
        if not v or not v.strip():
            raise ValueError("Formação acadêmica não pode estar vazia")
        
        clean_edu = v.strip()
        if len(clean_edu) < 10:
            raise ValueError(
                "Formação acadêmica deve ser mais detalhada. "
                "Inclua curso, instituição e período (mínimo 10 caracteres)."
            )
            
        return clean_edu

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v):
        if not v or not v.strip():
            raise ValueError("Habilidades não podem estar vazias")
        
        clean_skills = v.strip()
        if len(clean_skills) < 10:
            raise ValueError(
                "Liste suas habilidades de forma mais detalhada. "
                "Inclua tecnologias, ferramentas e competências (mínimo 10 caracteres)."
            )
            
        return clean_skills
        if len(v.split()) < 2:
            raise ValueError("Por favor, forneça nome e sobrenome")
        return v.title()  # Capitaliza as primeiras letras

    @model_validator(mode="before")
    @classmethod
    def validate_contact(cls, data):
        if isinstance(data, dict):
            email = data.get("email")
            phone = data.get("phone")
            
            # Pelo menos um meio de contato deve ser fornecido
            if not email and not phone:
                raise ValueError(
                    "Pelo menos um meio de contato deve ser fornecido. "
                    "Adicione um email válido ou número de telefone."
                )
                
            # Se ambos estão vazios ou são strings vazias
            if (email == "" or email is None) and (phone == "" or phone is None):
                raise ValueError(
                    "Os campos de contato não podem estar vazios. "
                    "Preencha pelo menos o email ou telefone."
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
