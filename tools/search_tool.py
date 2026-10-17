"""
Tool 1: DuckDuckGo web search wrapper.
Returns a list of {"title": ..., "url": ..., "snippet": ...} dicts.
"""

import json
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool


# num_results is supported; output_format="list" was removed in newer versions
_ddg = DuckDuckGoSearchResults(num_results=5)


@tool
def web_search(query: str) -> list[dict]:
    """
    Search the web using DuckDuckGo for the given query.
    Returns a list of results with title, url, and snippet.
    """
    try:
        raw = _ddg.invoke(query)

        # Newer langchain-community returns a JSON string — parse it
        if isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
            # Last resort: return as single snippet
            return [{"title": "Result", "url": "", "snippet": raw[:2000]}]

        if isinstance(raw, list):
            return raw

        return [{"title": "Result", "url": "", "snippet": str(raw)}]

    except Exception as e:
        return [{"title": "Error", "url": "", "snippet": f"Search failed: {str(e)}"}]
