from google import genai
from app.core.config import GEMINI_API_KEY

# New correct package
client = genai.Client(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> str:
    """
    Sends prompt to Gemini 2.5 Flash.
    Returns response text or None if failed.
    """
    try:
        print("Calling Gemini 2.5 Flash...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("Gemini responded successfully!")
        return response.text

    except Exception as e:
        print(f"Gemini failed: {e}")
        return None