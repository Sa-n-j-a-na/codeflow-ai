from groq import Groq
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

# Groq token limit — keep under 90K tokens to be safe
# 1 token ≈ 4 characters → 90K tokens ≈ 360K characters
MAX_PROMPT_CHARS = 360_000

def call_groq(prompt: str) -> str:
    """
    Sends prompt to Groq Llama 3.3 70B.
    Trims prompt if too large for Groq limit.
    """
    try:
        print("Calling Groq Llama 3.3...")

        # Trim if too large
        if len(prompt) > MAX_PROMPT_CHARS:
            print(f"Prompt too large ({len(prompt):,} chars) — trimming for Groq...")
            # Keep the prompt instructions (first 10K) + as much code as fits
            instructions = prompt[:10_000]
            code_budget = MAX_PROMPT_CHARS - 10_000
            code_section = prompt[10_000:10_000 + code_budget]
            prompt = instructions + code_section + "\n\n[NOTE: Codebase was trimmed to fit model limit]"
            print(f"Trimmed to {len(prompt):,} chars")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior software architect. Always respond with valid JSON only. No markdown, no explanation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )
        print("Groq responded successfully!")
        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq failed: {e}")
        return None


def call_ai(prompt: str) -> str:
    """
    Smart router — tries Gemini first, Groq as fallback.
    """
    from app.agent.models.gemini import call_gemini

    result = call_gemini(prompt)

    if not result:
        print("Falling back to Groq...")
        result = call_groq(prompt)

    return result