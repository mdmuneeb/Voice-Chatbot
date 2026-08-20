from fastapi import APIRouter, HTTPException, Request

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.llm_service import generate_response
from backend.app.services.tts_service import text_to_speech


router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest,
    http_request: Request
):

    try:

        # Step 1: LLM
        response_text = generate_response(
            request.message
        )

        # Step 2: Piper TTS
        audio_filename = text_to_speech(
            response_text
        )

        # Step 3: Create audio URL
        audio_url = (
            str(http_request.base_url)
            + f"audio/{audio_filename}"
        )

        # Step 4: Return response
        return ChatResponse(
            message=request.message,
            response=response_text,
            audio_file=audio_url,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )