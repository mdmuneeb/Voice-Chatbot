from langchain_core.messages import (
    HumanMessage,
    AIMessage,
)

from backend.app.graph.state import ChatState

from backend.app.services.supabase_service import (
    get_messages,
    save_message,
)

from backend.app.services.llm_service import (
    generate_response,
)

from backend.app.services.tts_service import (
    text_to_speech,
)

from backend.app.services.supabase_service import upload_audio


def chat_node(state: ChatState):

    thread_id = state["thread_id"]

    user_message = state["user_message"]

    previous_messages = get_messages(
        thread_id
    )

    messages = []

    for message in previous_messages:

        if message["role"] == "user":

            messages.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        elif message["role"] == "assistant":

            messages.append(
                AIMessage(
                    content=message["content"]
                )
            )

    messages.append(
        HumanMessage(
            content=user_message
        )
    )

    response_text = generate_response(
        messages
    )

    save_message(
        thread_id=thread_id,
        role="user",
        content=user_message,
    )

    return {
        "llm_response": response_text
    }

def piper_node(state: ChatState):
    

    text = state["llm_response"]

    thread_id = state["thread_id"]

    # Generate WAV
    audio_path = text_to_speech(
        text
    )

    # Upload WAV to Supabase
    audio_url = upload_audio(
        file_path=str(audio_path),
        thread_id=thread_id,
    )

    return {
        "audio_file": audio_url
    }


def save_assistant_node(state: ChatState):

    save_message(
        thread_id=state["thread_id"],
        role="assistant",
        content=state["llm_response"],
        audio_url=state["audio_file"],
    )

    return {}