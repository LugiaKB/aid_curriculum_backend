import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
