import os

from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path



load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)


# -------------------------
# Threads
# -------------------------

def create_thread(title: str):

    result = (
        supabase
        .table("threads")
        .insert({
            "title": title
        })
        .execute()
    )

    return result.data[0]


def get_threads():

    result = (
        supabase
        .table("threads")
        .select("*")
        .order(
            "updated_at",
            desc=True
        )
        .execute()
    )

    return result.data


def get_thread(thread_id: str):

    result = (
        supabase
        .table("threads")
        .select("*")
        .eq("id", thread_id)
        .single()
        .execute()
    )

    return result.data


# -------------------------
# Messages
# -------------------------

def get_messages(thread_id: str):

    result = (
        supabase
        .table("messages")
        .select("*")
        .eq("thread_id", thread_id)
        .order("created_at")
        .execute()
    )

    return result.data


def save_message(
    thread_id: str,
    role: str,
    content: str,
    audio_url: str | None = None,
):

    result = (
        supabase
        .table("messages")
        .insert({
            "thread_id": thread_id,
            "role": role,
            "content": content,
            "audio_url": audio_url,
        })
        .execute()
    )

    return result.data[0]

def upload_audio(
    file_path: str,
    thread_id: str,
):

    file_path = Path(file_path)

    storage_path = (
        f"{thread_id}/{file_path.name}"
    )

    with open(file_path, "rb") as file:

        supabase.storage \
            .from_("Audio") \
            .upload(
                storage_path,
                file,
                {
                    "content-type": "audio/wav"
                }
            )

    audio_url = (
        supabase.storage.from_("Audio")
        .get_public_url(
            storage_path
        )
    )

    return audio_url