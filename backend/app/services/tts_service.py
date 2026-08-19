import subprocess
import uuid

from backend.app.core.config import (
    PIPER_EXECUTABLE,
    PIPER_MODEL,
    AUDIO_DIR,
)


def text_to_speech(text: str) -> str:

    filename = f"{uuid.uuid4()}.wav"

    output_file = AUDIO_DIR / filename

    command = [
        str(PIPER_EXECUTABLE),
        "--model",
        str(PIPER_MODEL),
        "--output_file",
        str(output_file),
    ]

    result = subprocess.run(
        command,
        input=text,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Piper TTS failed: {result.stderr}"
        )

    return filename