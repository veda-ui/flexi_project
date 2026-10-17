"""
Agent 2: Researcher & Extractor
Executes web searches and scrapes content from the top results.
Uses DuckDuckGo search + Trafilatura scraper tools via LangChain.
"""

import json
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from utils.llm_config import get_llm
from tools.search_tool import web_search
from tools.scraper_tool import scrape_page

SYSTEM_PROMPT = """You are a web research agent. For each search query you receive:
1. Use the web_search tool to find relevant pages.
2. Pick the top 2-3 most relevant URLs from the results.
3. Use the scrape_page tool on each URL to extract content.
4. Return ALL successfully scraped content.

Be thorough — use both tools for each query provided. Focus on authoritative, content-rich pages.
Ignore results that seem like ads, homepages, or very short pages.
"""

TOOLS = [web_search, scrape_page]


def run_researcher(queries: list[str], status_callback=None) -> list[dict]:
    """
    Executes searches and scrapes content for each query using LangChain tool-calling loop.

    Args:
        queries: List of search query strings from Agent 1.
        status_callback: Optional callable(msg: str) for UI streaming.

    Returns:
        List of {"url": str, "title": str, "content": str} dicts.
    """
    llm = get_llm().bind_tools(TOOLS)
    all_results: list[dict] = []
    tool_map = {t.name: t for t in TOOLS}

    for query in queries:
        if status_callback:
            status_callback(f"[Agent 2] Searching web for: \"{query}\"...")

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Research this query thoroughly: {query}"),
        ]

        # Agentic tool-calling loop — runs until the LLM stops calling tools
        max_iterations = 6
        iteration = 0
        scraped_this_query = []

        while iteration < max_iterations:
            iteration += 1
            response = llm.invoke(messages)
            messages.append(AIMessage(content=response.content, tool_calls=response.tool_calls))

            if not response.tool_calls:
                # LLM finished — no more tool calls
                break

            for tc in response.tool_calls:
                tool_name = tc["name"]
                tool_args = tc["args"]
                tool_id = tc["id"]

                try:
                    result = tool_map[tool_name].invoke(tool_args)
                except Exception as e:
                    result = {"error": str(e)}

                # Collect scrape results
                if tool_name == "scrape_page" and isinstance(result, dict):
                    if result.get("success") and result.get("content"):
                        # Find title from search results if possible
                        scraped_this_query.append({
                            "url": result.get("url", tool_args.get("url", "")),
                            "title": f"Source for: {query}",
                            "content": result["content"],
                        })
                        if status_callback:
                            status_callback(
                                f"[Agent 2] ✓ Extracted {len(result['content'])} chars from {result.get('url', '')}"
                            )

                # Feed tool output back to LLM
                messages.append(
                    ToolMessage(
                        content=json.dumps(result) if not isinstance(result, str) else result,
                        tool_call_id=tool_id,
                    )
                )

        all_results.extend(scraped_this_query)

    if status_callback:
        status_callback(
            f"[Agent 2] ✓ Done. Extracted content from {len(all_results)} sources across {len(queries)} queries."
        )

    return all_results
