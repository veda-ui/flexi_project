"""
Agent 4: Summarizer
Drafts the final cohesive briefing document from the standardized data.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from utils.llm_config import get_llm

SYSTEM_PROMPT = """You are an expert research analyst and technical writer. You receive structured,
categorized research data and your job is to write a polished, professional briefing document.

Guidelines:
- Open with a concise executive summary (2-3 sentences).
- Present information in well-organized sections with clear ## headings.
- Highlight the 3-5 most important key takeaways in a dedicated section.
- Maintain a professional, neutral, and informative tone.
- Preserve all source citations from the input.
- End with a "## Conclusion" that synthesizes insights.
- Output ONLY the final Markdown report. No meta-commentary.
"""


def run_summarizer(structured_data: str, topic: str, status_callback=None) -> str:
    """
    Drafts the final briefing Markdown document.

    Args:
        structured_data: The standardized Markdown from Agent 3.
        topic: The original research topic.
        status_callback: Optional callable(msg: str) for UI streaming.

    Returns:
        Final Markdown report string.
    """
    if status_callback:
        status_callback("[Agent 4] Drafting final summary...")

    llm = get_llm()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""Please write a comprehensive briefing document on the topic: "{topic}"

Using this structured research data:

{structured_data}"""
        ),
    ]

    response = llm.invoke(messages)
    report = response.content.strip()

    if status_callback:
        status_callback("[Agent 4] ✓ Final briefing document ready!")

    return report
