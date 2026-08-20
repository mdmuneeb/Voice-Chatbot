from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_DIR = Path(__file__).resolve().parents[3]

load_dotenv(PROJECT_DIR / ".env")


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


PIPER_EXECUTABLE = (
    PROJECT_DIR
    / ".venv"
    / "Scripts"
    / "piper.exe"
)


PIPER_MODEL = (
    PROJECT_DIR
    / "backend"
    / "models"
    / "en_US-lessac-medium.onnx"
)


AUDIO_DIR = (
    PROJECT_DIR
    / "backend"
    / "audio"
)

AUDIO_DIR.mkdir(exist_ok=True)