import json

from app.agent.models.gemini import call_gemini
from app.agent.prompts import ARCHITECTURE_DISCOVERY_PROMPT


def extract_architecture(
    structure: str,
    content: str
) -> dict:

    print("\n[Architecture Discovery]")

    prompt = ARCHITECTURE_DISCOVERY_PROMPT
    prompt = prompt.replace("{structure}", structure)
    prompt = prompt.replace("{content}", content[:80000])

    raw = call_gemini(prompt)

    if not raw:
        return {
            "project_type": "Unknown",
            "project_summary": "",
            "features": [],
            "user_journeys": [],
            "services": [],
            "data_entities": [],
            "external_systems": [],
            "entry_points": []
        }

    try:
        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")

        return json.loads(raw)

    except Exception as e:
        print("Architecture parse failed:", e)

        return {
            "project_type": "Unknown",
            "project_summary": "",
            "features": [],
            "user_journeys": [],
            "services": [],
            "data_entities": [],
            "external_systems": [],
            "entry_points": []
        }