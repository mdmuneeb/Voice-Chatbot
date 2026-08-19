import requests
from dotenv import load_dotenv
import os 

API_KEY = os.getenv("OPENROUTER_API_KEY")

load_dotenv()

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

models = response.json()

for model in models["data"]:
    if ":free" in model["id"]:
        print(model["id"])
