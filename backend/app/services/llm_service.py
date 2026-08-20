import os

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI


load_dotenv()


llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    # model="nvidia/nemotron-3.5-lightning:free",
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


SYSTEM_PROMPT = """
You are a voice assistant.

Your responses will be converted into speech using a text-to-speech system.

Follow these rules:

- Respond in simple, natural English.
- Keep responses concise and conversational.
- Do not use Markdown.
- Do not use bullet points.
- Do not use headings.
- Do not use emojis.
- Do not use unnecessary special characters.
- Avoid long lists.
- Write exactly what a person would naturally say aloud.
- Prefer short and clear sentences.
"""


def generate_response(messages):

    formatted_messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        )
    ]

    formatted_messages.extend(messages)

    response = llm.invoke(
        formatted_messages
    )

    return response.content.strip()