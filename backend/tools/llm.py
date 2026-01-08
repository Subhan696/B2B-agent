import google.generativeai as genai
import os

def generate_content(prompt: str) -> str:
    """
    Generates content using Gemini, trying multiple model versions.
    Requires GEMINI_API_KEY in environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not set. Please set it in .env file."
    
    try:
        genai.configure(api_key=api_key)
        
        # Comprehensive list of potential model names based on user availability
        models_to_try = [
            'models/gemini-2.0-flash',
            'models/gemini-2.5-flash',
            'models/gemini-flash-latest',
            'models/gemini-2.0-flash-001',
            'gemini-2.0-flash',
            'gemini-2.5-flash',
            'models/gemini-1.5-flash', # Fallback
            'gemini-1.5-flash'
        ]
        
        last_error = None
        
        print(f"LLM: Starting generation with API Key ending in ...{str(api_key)[-4:]}")
        
        for model_name in models_to_try:
            try:
                print(f"LLM: Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                print(f"LLM: Success with {model_name}")
                return response.text
            except Exception as e:
                print(f"LLM: Failed with {model_name}: {e}")
                last_error = e
                continue
                
        return f"LLM Error: Could not generate content with any model. Last error: {last_error}"
    except Exception as e:
        return f"LLM Configuration Error: {e}"
