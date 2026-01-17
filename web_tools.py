# web_tools.py
import requests

def web_search(query: str) -> str:
    """
    Very basic web fetch.
    Replace with Antigravity / Google Search API when ready.
    """
    url = f"https://duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(url, timeout=5)
        return f"Search performed for query: {query}"
    except Exception as e:
        return f"Web search failed: {e}"
