from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="CV Generator API",
    description="API for generating CVs using Google's Gemini AI",
    version="0.1.0",
)

app.include_router(router)
