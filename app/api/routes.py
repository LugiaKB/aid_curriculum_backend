from fastapi import APIRouter
from app.schemas.cv import CVRequest
from app.integrations.gemini.service import GeminiService

router = APIRouter()
gemini_service = GeminiService()


@router.post("/generate-cv")
def generate_cv(cv_request: CVRequest):
    """
    Generate a CV based on user input using Gemini AI
    """
    return gemini_service.generate_cv(cv_request)
