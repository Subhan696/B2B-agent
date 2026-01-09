from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'} ({api_key[-4:] if api_key else 'N/A'})")

try:
    client = genai.Client(api_key=api_key)
    
    model_name = "gemini-3-flash-preview"
    print(f"\nTesting '{model_name}'...")
    
    response = client.models.generate_content(
        model=model_name,
        contents="Hello, this is a test check."
    )
    print(f"SUCCESS! Response: {response.text}")

except Exception as e:
    print(f"FAILED: {e}")
