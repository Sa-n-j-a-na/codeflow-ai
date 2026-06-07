import json
import re

def parse_ai_response(raw_response: str) -> dict:
    """
    Parses raw AI response into clean flow JSON.
    Handles cases where AI wraps response in markdown.
    """
    try:
        # Remove markdown code fences if AI added them
        # AI sometimes returns ```json ... ``` even when told not to
        clean = re.sub(r"```json|```", "", raw_response).strip()

        # Parse JSON
        flow_data = json.loads(clean)
        return flow_data

    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        print(f"Raw response preview: {raw_response[:200]}")
        return {
            "error": "AI returned invalid JSON",
            "raw_preview": raw_response[:500]
        }

    except Exception as e:
        return {
            "error": f"Parse failed: {str(e)}"
        }


def auto_layout(flow_data: dict) -> dict:
    """
    Automatically positions nodes if positions are missing.
    Creates a clean grid layout.
    """
    nodes = flow_data.get("nodes", [])

    HORIZONTAL_SPACING = 280
    VERTICAL_SPACING = 160
    COLUMNS = 4
    START_X = 100
    START_Y = 100

    for i, node in enumerate(nodes):
        # Only set position if missing or zero
        if not node.get("position") or (
            node["position"].get("x") == 0 and
            node["position"].get("y") == 0
        ):
            col = i % COLUMNS
            row = i // COLUMNS
            node["position"] = {
                "x": START_X + col * HORIZONTAL_SPACING,
                "y": START_Y + row * VERTICAL_SPACING
            }

    flow_data["nodes"] = nodes
    return flow_data