from typing import Dict
from app.schemas.cv import CVRequest, CVResponse
from app.integrations.gemini.client import GeminiClient


class GeminiService:

    BASE_SYSTEM_INSTRUCTION = """
    You are an expert CV generator and career advisor with deep knowledge of the tech industry. Your task is to:

    1. ANALYZE THE INPUT:
    - Process informal, conversational descriptions of career history
    - Identify key skills, achievements, and experiences
    - Extract project information and technical details when provided
    - If a target job description is provided, analyze requirements and match them with the candidate's profile

    2. GENERATE CV:
    - Transform casual language into powerful professional statements
    - Extract and highlight quantifiable achievements
    - Structure information in a clear, professional format
    - Ensure all statements are impactful but truthful to the original input
    - Add relevant implied skills and achievements based on the descriptions
    - Include project details with technologies used and links when available

    3. WHEN TARGET JOB IS PROVIDED:
    - Calculate compatibility score based on:
        * Direct skill matches
        * Related/transferable skills
        * Experience level alignment
        * Industry knowledge
        * Relevant projects
    - Identify skill gaps
    - Provide specific, actionable improvement suggestions
    - Recommend learning resources (courses, tutorials, documentation)
    - Focus CV content to highlight relevant experience for the target role

    4. FORMAT THE RESPONSE:
    Your response must be a JSON object that matches the specified schema exactly.

    5. QUALITY STANDARDS:
    - All entries must be professional and polished
    - Include specific metrics and achievements where possible
    - Maintain truthfulness to original input while enhancing presentation
    - Ensure all URLs and resources are relevant and specific
    - Provide detailed, actionable improvement suggestions
    - Include project technologies in the technologies array
    
    6. PROJECTS SECTION:
    When project information is provided:
    - Extract project name, description, and technologies used
    - Include links to repositories or project sites when mentioned
    - Highlight the impact and technologies used in each project
    - Ensure technologies are listed as separate items in the array
    """

    def __init__(self):
        self.client = GeminiClient()

    def generate_cv(self, cv_request: CVRequest) -> Dict[str, str]:
        """
        Generate a CV using the Gemini model

        Args:
            cv_request (CVRequest): The CV request containing user information

        Returns:
            Dict[str, str]: A dictionary containing either the CV content or an error message
        """
        prompt = self._create_prompt(cv_request)
        content = self.client.generate_json_response(
            prompt=prompt,
            system_instruction=self.BASE_SYSTEM_INSTRUCTION,
            json_schema=CVResponse.model_json_schema(),
        )

        if isinstance(content, dict) and content.get("status") == "error":
            return {"error": content.get("message", "Failed to generate CV")}

        return {"cv_content": content}

    def _create_prompt(self, cv_request: CVRequest) -> str:
        """
        Create a prompt for CV generation from the request data

        Args:
            cv_request (CVRequest): The CV request containing user information

        Returns:
            str: The formatted prompt
        """
        sections = [
            "INFORMAÇÕES PESSOAIS:",
            f"Nome Completo: {cv_request.full_name}",
            f"Cargo Desejado: {cv_request.desired_role}",
        ]

        if cv_request.email:
            sections.append(f"Email: {cv_request.email}")
        if cv_request.phone:
            sections.append(f"Telefone: {cv_request.phone}")

        sections.extend(
            [
                "",
                "EXPERIÊNCIA PROFISSIONAL (descrição informal):",
                cv_request.professional_experience,
            ]
        )

        if cv_request.projects:
            sections.extend(
                [
                    "",
                    "PROJETOS (descrição informal de projetos pessoais/acadêmicos):",
                    cv_request.projects,
                ]
            )

        sections.extend(
            [
                "",
                "FORMAÇÃO ACADÊMICA (descrição informal):",
                cv_request.education,
                "",
                "HABILIDADES E COMPETÊNCIAS (descrição informal):",
                cv_request.skills,
            ]
        )

        if cv_request.target_job_description:
            sections.extend(
                [
                    "",
                    "DESCRIÇÃO DA VAGA ALVO:",
                    cv_request.target_job_description,
                    "",
                    "INSTRUÇÕES ESPECIAIS:",
                    "- Compare as habilidades e experiências do candidato com os requisitos da vaga",
                    "- Calcule a compatibilidade e identifique gaps",
                    "- Forneça sugestões específicas de desenvolvimento",
                    "- Recomende recursos de aprendizado relevantes",
                    "- Estruture o CV destacando pontos relevantes para esta vaga",
                ]
            )

        cv_data = "\n".join(sections)

        return f"""Por favor, analise as seguintes informações fornecidas de forma casual/informal 
e transforme-as em um currículo profissional estruturado.

{cv_data}

OBSERVAÇÕES IMPORTANTES:
1. Extraia conquistas e métricas implícitas no texto
2. Expanda descrições breves que pareçam importantes
3. Mantenha a veracidade das informações enquanto melhora a apresentação
4. Use linguagem profissional e impactante
5. Estruture o conteúdo de forma clara e organizada
6. Identifique e explicite tanto habilidades técnicas quanto comportamentais

Forneça a resposta no formato JSON conforme especificado nas instruções do sistema."""

    def _format_list(self, items: list[str]) -> str:
        """Format a list of items into a bullet-point string"""
        return "\n".join(f"- {item}" for item in items)
