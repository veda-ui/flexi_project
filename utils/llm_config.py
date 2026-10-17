"""
LLM configuration — points OpenAI SDK to the Ollama cloud endpoint.
Shared across all agents.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

MODEL_NAME = "gpt-oss:20b"

def get_llm(streaming: bool = False) -> ChatOpenAI:
    """Return a ChatOpenAI instance wired to the Ollama cloud endpoint."""
    return ChatOpenAI(
        model=MODEL_NAME,
        base_url=os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1"),
        api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        temperature=0.3,
        streaming=streaming,
    )
