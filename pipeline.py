"""
Pipeline Orchestrator
Chains all 4 agents in sequence and streams status updates to a callback.
"""

from agents.query_formulator import run_query_formulator
from agents.researcher import run_researcher
from agents.standardizer import run_standardizer
from agents.summarizer import run_summarizer


def run_pipeline(topic: str, status_callback=None) -> dict:
    """
    Executes the full 4-agent research pipeline sequentially.

    Args:
        topic: The broad research topic provided by the user.
        status_callback: Optional callable(msg: str) — called with live status updates.

    Returns:
        A dict with keys:
            - "queries": list[str]
            - "raw_data": list[dict]
            - "structured": str (Markdown)
            - "report": str (final Markdown briefing)
    """

    def _cb(msg: str):
        if status_callback:
            status_callback(msg)

    _cb(f"🚀 Starting research pipeline for: \"{topic}\"")

    # ── Agent 1: Query Formulation ─────────────────────────────────────────────
    _cb("\n─── Agent 1: Query Formulator ───")
    queries = run_query_formulator(topic, status_callback=_cb)

    if not queries:
        raise ValueError("Agent 1 produced no queries. Check the LLM connection.")

    # ── Agent 2: Research & Extraction ────────────────────────────────────────
    _cb("\n─── Agent 2: Researcher & Extractor ───")
    raw_data = run_researcher(queries, status_callback=_cb)

    if not raw_data:
        _cb("[Warning] Agent 2 extracted no content. Proceeding with empty data.")

    # ── Agent 3: Standardization ──────────────────────────────────────────────
    _cb("\n─── Agent 3: Standardizer ───")
    structured = run_standardizer(raw_data, topic, status_callback=_cb)

    # ── Agent 4: Summarization ────────────────────────────────────────────────
    _cb("\n─── Agent 4: Summarizer ───")
    report = run_summarizer(structured, topic, status_callback=_cb)

    _cb("\n✅ Pipeline complete!")

    return {
        "queries": queries,
        "raw_data": raw_data,
        "structured": structured,
        "report": report,
    }
