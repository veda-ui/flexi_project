"""
Agent 1: Query Formulator
Analyzes the user's broad topic and returns a JSON array of targeted search queries.
"""

import json
from langchain_core.messages import HumanMessage, SystemMessage
from utils.llm_config import get_llm

SYSTEM_PROMPT = """You are a research query expert. Your job is to analyze a broad user topic
and decompose it into 4-5 precise, targeted search queries that together cover the topic thoroughly.

Rules:
- Output ONLY a valid JSON array of strings. No explanations, no markdown, no extra text.
- Each query should target a different facet (e.g., recent news, technical details, key players, history, future outlook).
- Queries should be specific and search-engine optimized.

Example output for topic "solid-state batteries":
["solid state battery breakthroughs 2024 2025", "solid state battery energy density comparison lithium ion", "solid state battery manufacturers Toyota QuantumScape timeline", "solid state battery challenges commercialization", "solid state battery EV market adoption forecast"]
"""


def run_query_formulator(topic: str, status_callback=None) -> list[str]:
    """
    Takes a user topic and returns a list of search queries.

    Args:
        topic: The broad research topic from the user.
        status_callback: Optional callable(msg: str) to stream status to UI.

    Returns:
        List of search query strings.
    """
    if status_callback:
        status_callback(f"[Agent 1] Analyzing topic: \"{topic}\"...")

    llm = get_llm()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Topic: {topic}"),
    ]

    response = llm.invoke(messages)
    raw = response.content.strip()

    # Parse JSON array from response
    try:
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        queries = json.loads(raw.strip())
        if not isinstance(queries, list):
            raise ValueError("Expected a JSON array")
    except Exception:
        # Fallback: split by newline if JSON parse fails
        queries = [line.strip().strip('"').strip("'") for line in raw.split("\n") if line.strip()]
        queries = [q for q in queries if len(q) > 5][:5]

    if status_callback:
        status_callback(f"[Agent 1] Generated {len(queries)} queries: {json.dumps(queries)}")

    return queries
