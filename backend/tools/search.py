from duckduckgo_search import DDGS
from typing import List, Dict

def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Performs a DuckDuckGo search and returns results.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []
