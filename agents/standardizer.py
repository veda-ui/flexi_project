"""
Agent 3: Standardizer
Cleans and structures raw extracted text into a well-organized Markdown document
with categorized sections and source citations.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from utils.llm_config import get_llm

SYSTEM_PROMPT = """You are a research data standardizer. You receive raw text extracted from multiple web sources
on a given topic. Your job is to:

1. Deduplicate overlapping information.
2. Organize facts into 3-5 logical categories/sections (e.g., "Overview", "Key Developments", "Challenges", "Future Outlook").
3. Format each section clearly with bullet points.
4. Attach a [Source N] citation tag to each fact, mapping it to the provided source URLs.
5. Fix broken encoding, remove irrelevant noise (ads, navigation text, etc.).

Output ONLY a clean Markdown document with:
- A "## Sources" section at the end listing all URLs.
- No preamble or meta-commentary.
"""


def run_standardizer(raw_data: list[dict], topic: str, status_callback=None) -> str:
    """
    Cleans and structures raw research data.

    Args:
        raw_data: List of {"url": str, "title": str, "content": str} dicts from Agent 2.
        topic: The original research topic (for context).
        status_callback: Optional callable(msg: str) for UI streaming.

    Returns:
        A structured Markdown string.
    """
    if status_callback:
        status_callback(f"[Agent 3] Standardizing {len(raw_data)} sources...")

    # Build the input document for the LLM
    sources_text = ""
    for i, item in enumerate(raw_data, 1):
        sources_text += f"\n---\n### Source {i}: {item.get('title', 'Unknown')}\nURL: {item.get('url', '')}\n\n{item.get('content', '')}\n"

    user_message = f"""Topic: {topic}

Raw Extracted Data:
{sources_text}

Please standardize and structure this into a clean Markdown document."""

    if status_callback:
        status_callback("[Agent 3] Cleaning data... removing duplicates and organizing categories...")

    llm = get_llm()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages)
    structured = response.content.strip()

    if status_callback:
        status_callback("[Agent 3] ✓ Data standardized and structured successfully.")

    return structured
