from fastapi import APIRouter, HTTPException

from backend.app.schemas.thread import (
    ThreadCreate,
    ThreadResponse,
)

from backend.app.services.supabase_service import (
    create_thread,
    get_threads,
    get_thread,
)


router = APIRouter(
    prefix="/api/threads",
    tags=["Threads"],
)


@router.post(
    "",
    response_model=ThreadResponse
)
async def new_thread(
    request: ThreadCreate
):

    try:

        thread = create_thread(
            request.title
        )

        return ThreadResponse(
            id=thread["id"],
            title=thread["title"],
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("")
async def threads():

    try:

        return get_threads()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/{thread_id}")
async def thread(
    thread_id: str
):

    try:

        return get_thread(
            thread_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )