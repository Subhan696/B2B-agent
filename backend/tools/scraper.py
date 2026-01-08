import requests
from bs4 import BeautifulSoup
import asyncio

def scrape_url_sync(url: str) -> str:
    """
    Scrapes the content of a URL using requests (sync).
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:10000]
    except Exception as e:
        return f"Scraping Error: {e}"

async def scrape_url(url: str) -> str:
    """
    Async wrapper for sync scraper.
    """
    return await asyncio.to_thread(scrape_url_sync, url)
