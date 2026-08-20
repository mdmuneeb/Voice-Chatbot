from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from backend.app.graph.graph import graph


router = APIRouter(
    prefix="/api",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest
):

    try:

        result = graph.invoke({

            "thread_id":
                request.thread_id,

            "user_message":
                request.message,

        })


        return ChatResponse(

            thread_id=
                request.thread_id,

            message=
                request.message,

            response=
                result["llm_response"],

            audio_url=
                result["audio_file"],
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )