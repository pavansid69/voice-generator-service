# src/main.py
from fastapi import FastAPI
from src.routes.audio_routes import router as audio_router

app = FastAPI(title="Voice Generator Service")

app.include_router(audio_router, prefix="/api/v1")



