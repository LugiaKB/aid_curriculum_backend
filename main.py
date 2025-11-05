import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app.api.routes import router
from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="AId Curriculum API",
    description="API para geração de currículos utilizando um modelo de LLM avançado.",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler global para erros de validação do FastAPI/Pydantic
    """
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        
        # Personalizar mensagens mais amigáveis
        if "field required" in message.lower():
            message = "Este campo é obrigatório"
        elif "ensure this value has at least" in message.lower():
            message = "Este campo é muito curto"
        elif "invalid email format" in message.lower():
            message = "Formato de email inválido"
            
        error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Erro de validação",
            "message": "Os dados fornecidos contêm erros. Verifique os campos abaixo:",
            "details": error_messages,
            "help": "Certifique-se de que todos os campos obrigatórios estão preenchidos corretamente."
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """
    Handler específico para erros de validação do Pydantic
    """
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"]) if error["loc"] else "dados"
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Erro de validação",
            "message": "Os dados fornecidos não atendem aos critérios necessários",
            "details": error_messages
        }
    )


# Include routes
app.include_router(router, prefix="/api/v1")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Root endpoint with API information
@app.get("/")
async def root():
    return {
        "name": "CV Generator API",
        "version": "0.1.0",
        "documentation": "/docs",
        "openapi": "/openapi.json",
    }


if __name__ == "__main__":
    # Validate that the GOOGLE_API_KEY is set before starting the server
    if not settings.google_api_key:
        print("ERROR: GOOGLE_API_KEY não encontrada nas variáveis de ambiente.")
        print(
            "1) Copie .env.example para .env e adicione sua key:\n   cp .env.example .env\n   (edite .env e defina GOOGLE_API_KEY=SUACHAVE)"
        )
        print(
            "2) Ou exporte no shell temporariamente:\n   export GOOGLE_API_KEY=SUACHAVE"
        )
        print("3) Inicie com pipenv para garantir o .env carregado:\n   pipenv run api")
        sys.exit(1)

    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
