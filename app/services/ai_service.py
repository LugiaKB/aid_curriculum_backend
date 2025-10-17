from typing import Optional, List, Dict
import json
from app.config import settings


class AIService:
    """Service for AI-powered resume generation and analysis."""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        self._client = None
    
    @property
    def client(self):
        """Lazy load OpenAI client."""
        if self._client is None and self.api_key:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                pass
        return self._client
    
    async def generate_resume_content(
        self,
        job_description: str,
        user_info: Optional[str] = None,
        experience_level: str = "mid-level",
        include_sections: List[str] = None
    ) -> Dict:
        """Generate resume content based on job description using AI."""
        
        if include_sections is None:
            include_sections = ["summary", "skills", "experience", "projects"]
        
        # Build prompt for AI
        prompt = self._build_generation_prompt(
            job_description, user_info, experience_level, include_sections
        )
        
        # If OpenAI is configured, use it
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert resume writer and career advisor. Generate professional resume content in JSON format."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                
                content = response.choices[0].message.content
                # Try to parse as JSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If not valid JSON, structure the response
                    return {"generated_text": content}
            except Exception as e:
                # Fall back to template-based generation
                return self._generate_template_content(
                    job_description, experience_level, include_sections
                )
        
        # Fall back to template-based generation if no API key
        return self._generate_template_content(
            job_description, experience_level, include_sections
        )
    
    async def analyze_resume(
        self,
        resume_content: str,
        job_description: Optional[str] = None
    ) -> Dict:
        """Analyze resume and provide feedback."""
        
        prompt = self._build_analysis_prompt(resume_content, job_description)
        
        # If OpenAI is configured, use it
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert resume reviewer and ATS specialist. Analyze resumes and provide actionable feedback in JSON format."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=1000
                )
                
                content = response.choices[0].message.content
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {
                        "score": 75.0,
                        "strengths": ["Well-formatted content"],
                        "improvements": ["Consider tailoring to specific job requirements"],
                        "suggestions": [content]
                    }
            except Exception as e:
                return self._generate_template_analysis(resume_content)
        
        # Fall back to template-based analysis
        return self._generate_template_analysis(resume_content)
    
    def _build_generation_prompt(
        self,
        job_description: str,
        user_info: Optional[str],
        experience_level: str,
        include_sections: List[str]
    ) -> str:
        """Build prompt for resume generation."""
        prompt = f"""Generate professional resume content for a {experience_level} candidate for the following job:

Job Description:
{job_description}

"""
        if user_info:
            prompt += f"""Candidate Information:
{user_info}

"""
        
        prompt += f"""Please generate content for these sections: {', '.join(include_sections)}

Return the response as a JSON object with the following structure:
{{
    "professional_summary": "2-3 sentence summary...",
    "skills": ["skill1", "skill2", ...],
    "experience_suggestions": ["suggestion1", "suggestion2", ...],
    "project_ideas": ["project1", "project2", ...]
}}"""
        
        return prompt
    
    def _build_analysis_prompt(
        self,
        resume_content: str,
        job_description: Optional[str]
    ) -> str:
        """Build prompt for resume analysis."""
        prompt = f"""Analyze the following resume and provide detailed feedback:

Resume:
{resume_content}

"""
        if job_description:
            prompt += f"""Target Job Description:
{job_description}

"""
        
        prompt += """Provide analysis in JSON format with:
{{
    "score": (0-100),
    "strengths": ["strength1", "strength2", ...],
    "improvements": ["improvement1", "improvement2", ...],
    "keywords_match": {{"matched": ["keyword1"], "missing": ["keyword2"]}},
    "suggestions": ["suggestion1", "suggestion2", ...]
}}"""
        
        return prompt
    
    def _generate_template_content(
        self,
        job_description: str,
        experience_level: str,
        include_sections: List[str]
    ) -> Dict:
        """Generate template-based content when AI is not available."""
        content = {}
        
        if "summary" in include_sections:
            content["professional_summary"] = (
                f"Motivated {experience_level} professional with strong technical skills "
                "and a passion for delivering high-quality results. Experienced in problem-solving "
                "and collaborating with cross-functional teams."
            )
        
        if "skills" in include_sections:
            content["skills"] = [
                "Python", "JavaScript", "Problem Solving",
                "Team Collaboration", "Communication", "Project Management"
            ]
        
        if "experience" in include_sections:
            content["experience_suggestions"] = [
                "Highlight quantifiable achievements (e.g., 'Improved performance by 30%')",
                "Use action verbs to describe responsibilities",
                "Focus on relevant experience for the target role"
            ]
        
        if "projects" in include_sections:
            content["project_ideas"] = [
                "Describe technical projects that demonstrate relevant skills",
                "Include technologies used and impact of the project",
                "Link to live demos or GitHub repositories if available"
            ]
        
        return content
    
    def _generate_template_analysis(self, resume_content: str) -> Dict:
        """Generate template-based analysis when AI is not available."""
        word_count = len(resume_content.split())
        
        return {
            "score": 70.0,
            "strengths": [
                "Resume contains substantial content" if word_count > 100 else "Concise presentation",
                "Structured information provided"
            ],
            "improvements": [
                "Consider adding quantifiable achievements",
                "Ensure keywords match job requirements",
                "Use action verbs to describe responsibilities"
            ],
            "keywords_match": {
                "matched": ["professional", "experience", "skills"],
                "missing": ["specific technical keywords from job description"]
            },
            "suggestions": [
                "Tailor your resume to each job application",
                "Use a clean, ATS-friendly format",
                "Include relevant certifications and education",
                "Proofread for grammar and spelling errors"
            ]
        }


# Singleton instance
ai_service = AIService()
