from typing import TypedDict


class ChatState(TypedDict):

    thread_id: str

    user_message: str

    llm_response: str

    audio_file: str