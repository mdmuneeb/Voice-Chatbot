from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.chat import router as chat_router
from backend.app.core.config import AUDIO_DIR


app = FastAPI(
    title="Voice Chatbot API",
    description="LLM powered voice chatbot",
    version="1.0.0",
)


# Serve generated audio files
app.mount(
    "/audio",
    StaticFiles(directory=AUDIO_DIR),
    name="audio",
)


# Register routes
app.include_router(chat_router)


@app.get("/")
async def root():

    return {
        "message": "Voice Chatbot API is running"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }