# architecture_extractor.py

import json

from app.agent.models.gemini import call_gemini
from app.agent.prompts import ARCHITECTURE_DISCOVERY_PROMPT
from app.agent.tools.static_analyzer import analyze_codebase


def _default_architecture():

    return {
        "project_type": "Unknown",
        "project_summary": "",
        "features": [],
        "user_journeys": [],
        "services": [],
        "data_entities": [],
        "external_systems": [],
        "entry_points": [],

        # NEW
        "static_analysis": {
            "apis": [],
            "services": [],
            "models": [],
            "dependencies": []
        },

        "summary": {
            "api_count": 0,
            "service_count": 0,
            "model_count": 0,
            "dependency_count": 0
        }
    }


def extract_architecture(
    structure: str,
    content: str,
    codebase_path: str = None
) -> dict:

    print("\n[Architecture Discovery]")

    static_data = {
        "apis": [],
        "services": [],
        "models": [],
        "dependencies": []
    }

    if codebase_path:
        try:
            static_data = analyze_codebase(codebase_path)
        except Exception as e:
            print("Static analysis failed:", e)

    prompt = ARCHITECTURE_DISCOVERY_PROMPT

    prompt = prompt.replace(
        "{structure}",
        structure
    )

    prompt = prompt.replace(
        "{content}",
        content[:80000]
    )

    prompt += f"""

STATIC ANALYSIS RESULTS

APIS
{json.dumps(static_data["apis"], indent=2)}

SERVICES
{json.dumps(static_data["services"], indent=2)}

MODELS
{json.dumps(static_data["models"], indent=2)}

DEPENDENCIES
{json.dumps(static_data["dependencies"][:100], indent=2)}

Use these facts while discovering architecture.
Do not ignore them.
"""

    raw = call_gemini(prompt)

    if not raw:
        architecture = _default_architecture()

        architecture["static_analysis"] = static_data

        architecture["summary"] = {
            "api_count": len(static_data["apis"]),
            "service_count": len(static_data["services"]),
            "model_count": len(static_data["models"]),
            "dependency_count": len(static_data["dependencies"])
        }

        return architecture

    try:

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")

        architecture = json.loads(raw)

        architecture["static_analysis"] = static_data

        architecture["summary"] = {
            "api_count": len(static_data["apis"]),
            "service_count": len(static_data["services"]),
            "model_count": len(static_data["models"]),
            "dependency_count": len(static_data["dependencies"])
        }

        return architecture

    except Exception as e:

        print("Architecture parse failed:", e)

        architecture = _default_architecture()

        architecture["static_analysis"] = static_data

        architecture["summary"] = {
            "api_count": len(static_data["apis"]),
            "service_count": len(static_data["services"]),
            "model_count": len(static_data["models"]),
            "dependency_count": len(static_data["dependencies"])
        }

        return architecture