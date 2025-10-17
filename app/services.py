from typing import List, Optional
import json
import logging
from app.models import ResumeData, ResumeGenerationRequest
from app.config import settings
from openai import OpenAI

# Configure logging
logger = logging.getLogger(__name__)


class AIResumeService:
    """Service for AI-powered resume generation"""
    
    def __init__(self):
        self.client = None
        if settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
    
    def _format_resume_data_for_prompt(self, resume_data: ResumeData) -> str:
        """Format resume data into a structured text for the AI prompt"""
        sections = []
        
        # Personal Info
        personal = resume_data.personal_info
        sections.append(f"**Personal Information:**")
        sections.append(f"Name: {personal.full_name}")
        sections.append(f"Email: {personal.email}")
        if personal.phone:
            sections.append(f"Phone: {personal.phone}")
        if personal.location:
            sections.append(f"Location: {personal.location}")
        if personal.linkedin:
            sections.append(f"LinkedIn: {personal.linkedin}")
        if personal.github:
            sections.append(f"GitHub: {personal.github}")
        if personal.website:
            sections.append(f"Website: {personal.website}")
        if personal.summary:
            sections.append(f"Summary: {personal.summary}")
        
        # Education
        if resume_data.education:
            sections.append("\n**Education:**")
            for edu in resume_data.education:
                sections.append(f"- {edu.degree} in {edu.field_of_study or 'N/A'} from {edu.institution}")
                if edu.start_date or edu.end_date:
                    sections.append(f"  Period: {edu.start_date or 'N/A'} - {edu.end_date or 'N/A'}")
                if edu.gpa:
                    sections.append(f"  GPA: {edu.gpa}")
                if edu.achievements:
                    sections.append(f"  Achievements: {', '.join(edu.achievements)}")
        
        # Experience
        if resume_data.experience:
            sections.append("\n**Work Experience:**")
            for exp in resume_data.experience:
                sections.append(f"- {exp.position} at {exp.company}")
                if exp.location:
                    sections.append(f"  Location: {exp.location}")
                if exp.start_date or exp.end_date:
                    sections.append(f"  Period: {exp.start_date or 'N/A'} - {exp.end_date or 'N/A'}")
                if exp.responsibilities:
                    sections.append("  Responsibilities:")
                    for resp in exp.responsibilities:
                        sections.append(f"    * {resp}")
        
        # Skills
        if resume_data.skills:
            sections.append("\n**Skills:**")
            for skill in resume_data.skills:
                sections.append(f"- {skill.category}: {', '.join(skill.items)}")
        
        # Certifications
        if resume_data.certifications:
            sections.append("\n**Certifications:**")
            for cert in resume_data.certifications:
                sections.append(f"- {cert}")
        
        # Languages
        if resume_data.languages:
            sections.append("\n**Languages:**")
            sections.append(f"{', '.join(resume_data.languages)}")
        
        return "\n".join(sections)
    
    def _build_system_prompt(self, request: ResumeGenerationRequest) -> str:
        """Build the system prompt for the AI"""
        tone_guidance = {
            "professional": "formal and professional tone, focusing on achievements and impact",
            "creative": "engaging and creative tone, showcasing personality and innovation",
            "technical": "technical and precise tone, emphasizing technical skills and methodologies"
        }
        
        style_guidance = {
            "modern": "Use a modern, clean format with clear sections and bullet points",
            "classic": "Use a traditional format with formal language and structured layout",
            "minimal": "Use a minimal, concise format focusing on key information only"
        }
        
        tone = tone_guidance.get(request.tone, tone_guidance["professional"])
        style = style_guidance.get(request.format_style, style_guidance["modern"])
        
        system_prompt = f"""You are a professional resume writer with expertise in creating compelling resumes.
Your task is to generate a well-structured, ATS-friendly resume in Markdown format.

Guidelines:
1. Use a {tone}
2. {style}
3. Highlight quantifiable achievements and impact
4. Use action verbs to start bullet points
5. Tailor the content to be relevant and impactful
6. Keep it concise yet comprehensive
7. Ensure proper formatting with clear section headers
8. Make it ATS (Applicant Tracking System) friendly

Resume Sections (in order):
1. Contact Information (name, email, phone, location, links)
2. Professional Summary (2-3 sentences highlighting key strengths)
3. Work Experience (most recent first, with bullet points)
4. Education (most recent first)
5. Skills (organized by category)
6. Certifications (if any)
7. Languages (if any)

Output the resume in clean Markdown format."""
        
        if request.target_role:
            system_prompt += f"\n\nTarget Role: Optimize the resume for a {request.target_role} position."
        
        return system_prompt
    
    def generate_resume(self, request: ResumeGenerationRequest) -> dict:
        """Generate a resume using AI"""
        if not self.client:
            # Fallback: Generate a basic resume without AI
            return self._generate_basic_resume(request)
        
        try:
            # Format the resume data
            resume_data_text = self._format_resume_data_for_prompt(request.resume_data)
            
            # Build prompts
            system_prompt = self._build_system_prompt(request)
            user_prompt = f"""Create a professional resume based on the following information:

{resume_data_text}

Generate the resume in Markdown format, making it compelling and ATS-friendly."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.openai_temperature,
                max_tokens=settings.openai_max_tokens
            )
            
            # Validate response
            if not response.choices:
                logger.warning("OpenAI returned empty response, using fallback")
                return self._generate_basic_resume(request)
            
            content = response.choices[0].message.content
            if not content:
                logger.warning("OpenAI returned empty content, using fallback")
                return self._generate_basic_resume(request)
            
            markdown_content = content.strip()
            
            # Generate suggestions
            suggestions = self._generate_suggestions(request.resume_data)
            
            return {
                "markdown_content": markdown_content,
                "html_content": None,  # Can be implemented with markdown to HTML converter
                "suggestions": suggestions
            }
        
        except Exception as e:
            # Fallback to basic resume on error
            logger.error(f"Error generating resume with AI: {e}")
            return self._generate_basic_resume(request)
    
    def _generate_basic_resume(self, request: ResumeGenerationRequest) -> dict:
        """Generate a basic resume without AI (fallback)"""
        resume_data = request.resume_data
        personal = resume_data.personal_info
        
        sections = []
        
        # Header
        sections.append(f"# {personal.full_name}\n")
        
        contact_info = []
        contact_info.append(personal.email)
        if personal.phone:
            contact_info.append(personal.phone)
        if personal.location:
            contact_info.append(personal.location)
        
        sections.append(" | ".join(contact_info))
        
        links = []
        if personal.linkedin:
            links.append(f"[LinkedIn]({personal.linkedin})")
        if personal.github:
            links.append(f"[GitHub]({personal.github})")
        if personal.website:
            links.append(f"[Website]({personal.website})")
        
        if links:
            sections.append(" | ".join(links))
        
        sections.append("\n---\n")
        
        # Professional Summary
        if personal.summary:
            sections.append("## Professional Summary\n")
            sections.append(f"{personal.summary}\n")
        
        # Work Experience
        if resume_data.experience:
            sections.append("## Work Experience\n")
            for exp in resume_data.experience:
                sections.append(f"### {exp.position}")
                company_info = [exp.company]
                if exp.location:
                    company_info.append(exp.location)
                sections.append(" | ".join(company_info))
                
                if exp.start_date or exp.end_date:
                    sections.append(f"*{exp.start_date or ''} - {exp.end_date or ''}*\n")
                
                if exp.responsibilities:
                    for resp in exp.responsibilities:
                        sections.append(f"- {resp}")
                sections.append("")
        
        # Education
        if resume_data.education:
            sections.append("## Education\n")
            for edu in resume_data.education:
                sections.append(f"### {edu.degree}")
                edu_info = [edu.institution]
                if edu.field_of_study:
                    edu_info.append(edu.field_of_study)
                sections.append(" | ".join(edu_info))
                
                if edu.start_date or edu.end_date:
                    sections.append(f"*{edu.start_date or ''} - {edu.end_date or ''}*")
                
                if edu.gpa:
                    sections.append(f"GPA: {edu.gpa}")
                
                if edu.achievements:
                    for achievement in edu.achievements:
                        sections.append(f"- {achievement}")
                sections.append("")
        
        # Skills
        if resume_data.skills:
            sections.append("## Skills\n")
            for skill in resume_data.skills:
                sections.append(f"**{skill.category}:** {', '.join(skill.items)}\n")
        
        # Certifications
        if resume_data.certifications:
            sections.append("## Certifications\n")
            for cert in resume_data.certifications:
                sections.append(f"- {cert}")
            sections.append("")
        
        # Languages
        if resume_data.languages:
            sections.append("## Languages\n")
            sections.append(", ".join(resume_data.languages))
            sections.append("")
        
        markdown_content = "\n".join(sections)
        suggestions = self._generate_suggestions(resume_data)
        
        return {
            "markdown_content": markdown_content,
            "html_content": None,
            "suggestions": suggestions
        }
    
    def _generate_suggestions(self, resume_data: ResumeData) -> List[str]:
        """Generate suggestions for resume improvement"""
        suggestions = []
        
        if not resume_data.personal_info.summary:
            suggestions.append("Consider adding a professional summary to highlight your key strengths and career objectives")
        
        if not resume_data.experience:
            suggestions.append("Add work experience to demonstrate your professional background")
        
        if not resume_data.skills:
            suggestions.append("Include relevant skills to showcase your technical and soft skills")
        
        if not resume_data.education:
            suggestions.append("Add your educational background to complete your profile")
        
        # Check for quantifiable achievements
        has_numbers = False
        for exp in resume_data.experience:
            for resp in exp.responsibilities:
                if any(char.isdigit() for char in resp):
                    has_numbers = True
                    break
        
        if not has_numbers and resume_data.experience:
            suggestions.append("Try to quantify your achievements with numbers, percentages, or metrics (e.g., 'Increased sales by 25%')")
        
        if len(suggestions) == 0:
            suggestions.append("Your resume looks comprehensive! Consider tailoring it for specific job applications")
        
        return suggestions


# Create a singleton instance
ai_resume_service = AIResumeService()
