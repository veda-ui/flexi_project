"""
Tool 2: Web page scraper using Trafilatura.
Given a URL, fetches and extracts the main textual content.
"""

import trafilatura
from langchain_core.tools import tool


@tool
def scrape_page(url: str) -> dict:
    """
    Fetch and extract the main textual content from a webpage URL.
    Returns a dict with keys: url, content (str), success (bool).
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return {"url": url, "content": "", "success": False}

        content = trafilatura.extract(
            downloaded,
            include_tables=False,
            include_comments=False,
            no_fallback=False,
        )

        if not content or len(content.strip()) < 50:
            return {"url": url, "content": "", "success": False}

        # Truncate to avoid overwhelming the LLM context
        return {"url": url, "content": content[:4000], "success": True}

    except Exception as e:
        return {"url": url, "content": f"Scrape failed: {str(e)}", "success": False}
