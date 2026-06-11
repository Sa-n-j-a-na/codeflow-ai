from groq import Groq
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def call_groq_model(prompt: str, model: str) -> str:
    try:
        print(f"  Calling Groq {model}...")
        print(f"  Prompt size: {len(prompt):,} chars (~{len(prompt)//4:,} tokens)")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior software architect. Respond with valid JSON only. No markdown, no explanation. Never truncate the JSON — always close all brackets and braces."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=4000  # ← force enough output tokens
        )
        print(f"  ✅ Groq {model} responded!")
        return response.choices[0].message.content

    except Exception as e:
        print(f"  ❌ Groq {model} failed: {e}")
        return None


def call_groq(prompt: str) -> str:
    # Try llama-3.3-70b first — better output, higher limits
    result = call_groq_model(prompt, "llama-3.3-70b-versatile")
    if result:
        return result
    # Fallback to 8b
    result = call_groq_model(prompt, "llama-3.1-8b-instant")
    return result


def call_ai(prompt: str) -> str:
    from app.agent.models.gemini import call_gemini
    result = call_gemini(prompt)
    if not result:
        print("  Falling back to Groq...")
        result = call_groq(prompt)
    return result


def call_ai_groq_only(prompt: str) -> str:
    return call_groq(prompt)