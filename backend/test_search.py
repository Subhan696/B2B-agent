from duckduckgo_search import DDGS
import json

print("Testing DuckDuckGo Search...")
try:
    results = DDGS().text("Stripe CEO", max_results=3)
    print(json.dumps(list(results), indent=2))
except Exception as e:
    print(f"Error: {e}")
