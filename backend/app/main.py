from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.chat import (
    router as chat_router
)

from backend.app.api.routes.threads import (
    router as threads_router
)


app = FastAPI(
    title="Voice Chatbot API"
)


# -------------------------
# Static audio files
# -------------------------

app.mount(
    "/audio",
    StaticFiles(
        directory="backend/audio"
    ),
    name="audio",
)


# -------------------------
# Routes
# -------------------------

app.include_router(
    chat_router
)

app.include_router(
    threads_router
)


@app.get("/")
async def root():

    return {
        "message": "Voice Chatbot API is running"
    }