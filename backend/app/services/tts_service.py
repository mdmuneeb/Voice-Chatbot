from pathlib import Path
import subprocess
import uuid


PROJECT_ROOT = Path(__file__).resolve().parents[3]


AUDIO_DIR = (
    PROJECT_ROOT
    / "backend"
    / "audio"
)


PIPER_EXECUTABLE = (
    PROJECT_ROOT
    / ".venv"
    / "Scripts"
    / "piper.exe"
)


PIPER_MODEL = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "en_US-lessac-medium.onnx"
)


AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def text_to_speech(text: str):

    filename = f"{uuid.uuid4()}.wav"

    output_path = AUDIO_DIR / filename

    command = [
        str(PIPER_EXECUTABLE),
        "--model",
        str(PIPER_MODEL),
        "--output_file",
        str(output_path),
    ]

    subprocess.run(
        command,
        input=text,
        text=True,
        check=True,
    )

    return output_path