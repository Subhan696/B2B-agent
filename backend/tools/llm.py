from google import genai
from google.genai import types
import os
import time
import random

def generate_content(prompt: str) -> str:
    """
    Generates content using the new Google GenAI SDK (v1).
    Uses 'gemini-3-flash-preview' as requested.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not set. Please set it in .env file."
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Explicitly using the user-requested model
        model_name = "gemini-3-flash-preview" 
        
        print(f"LLM: Starting generation with {model_name}...")

        # Retry loop for Rate Limiting
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                print(f"LLM: Success w/ {model_name}")
                return response.text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str:
                    wait_time = 10 + (attempt * 5)
                    print(f"LLM: 429 Rate Limit. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif "403" in error_str:
                    print("LLM Error: 403 Permission Denied. Check your API Key.")
                    return "LLM Error: API Key Invalid or Permissions Denied."
                else:
                    print(f"LLM Error: {e}")
                    raise e

    except Exception as e:
        return f"LLM Configuration Error: {e}"
