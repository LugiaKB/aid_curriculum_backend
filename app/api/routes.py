from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from app.schemas.cv import CVRequest
from app.integrations.gemini.service import GeminiService

router = APIRouter()
gemini_service = GeminiService()


@router.post("/generate-cv")
def generate_cv(cv_request: CVRequest):
    """
    Generate a CV based on user input using Gemini AI
    """
    try:
        return gemini_service.generate_cv(cv_request)
    except ValidationError as e:
        # Tratar erros de validação do Pydantic
        error_messages = []
        for error in e.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            error_messages.append(f"{field}: {message}")
        
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Erro de validação",
                "message": "Os dados fornecidos não são válidos",
                "details": error_messages
            }
        )
    except Exception as e:
        # Tratar outros erros inesperados
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno do servidor",
                "message": "Ocorreu um erro inesperado durante a geração do currículo",
                "details": str(e) if str(e) else "Erro desconhecido"
            }
        )
