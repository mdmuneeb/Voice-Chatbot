from langchain_core.messages import SystemMessage, HumanMessage

from backend.app.core.config import OPENROUTER_API_KEY
from langchain_openai import ChatOpenAI
import os


SYSTEM_PROMPT = """
You are a voice chatbot.

Your responses will be converted directly into speech using
a text-to-speech system.

Follow these rules:

- Respond naturally, like a human speaking.
- Do not use Markdown.
- Do not use bullet points.
- Do not use numbered lists.
- Do not use headings.
- Do not use asterisks.
- Do not use emojis.
- Do not use code blocks.
- Avoid unnecessary formatting.
- Keep responses concise and conversational.
- Use simple spoken language.
"""


llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    # model="nvidia/nemotron-3.5-lightning:free",
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def generate_response(user_message: str) -> str:

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]
    )

    return response.content