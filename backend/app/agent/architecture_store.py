import json
import os
import re
from datetime import datetime

STORE_DIR = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    ),
    "data", "architectures"
)


def get_project_id(source: str) -> str:
    clean = re.sub(r'https?://', '', source)
    clean = re.sub(r'[^a-zA-Z0-9]', '_', clean)
    clean = re.sub(r'_+', '_', clean)
    return clean.strip('_').lower()[:100]


def get_filepath(source: str) -> str:
    project_id = get_project_id(source)
    os.makedirs(STORE_DIR, exist_ok=True)
    return os.path.join(STORE_DIR, f"{project_id}.json")


def has_saved_diagram(source: str) -> bool:
    """Check if we already have a saved diagram for this project."""
    return os.path.exists(get_filepath(source))


def load_saved_diagram(source: str) -> dict:
    """Load the saved canonical diagram. Returns None if not found."""
    filepath = get_filepath(source)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"  Loaded saved diagram v{data.get('version', 1)}")
    return data


def save_diagram(source: str, flows: dict, diff: dict = None) -> dict:
    """
    Save the canonical diagram.
    First save = version 1
    Updates = increment version + store diff
    """
    filepath = get_filepath(source)
    existing = load_saved_diagram(source)

    version = 1 if not existing else existing.get("version", 1) + 1
    created_at = existing.get("created_at") if existing else datetime.now().isoformat()

    # Build diff history
    diff_history = existing.get("diff_history", []) if existing else []
    if diff and diff.get("has_changes"):
        diff_history.append({
            "version": version,
            "date": datetime.now().isoformat(),
            "changes": {
                "added": [n["label"] for n in diff.get("nodes", {}).get("added", [])],
                "removed": [n["label"] for n in diff.get("nodes", {}).get("removed", [])],
                "changed": [n["label"] for n in diff.get("nodes", {}).get("changed", [])]
            }
        })

    saved = {
        "project_id": get_project_id(source),
        "source": source,
        "created_at": created_at,
        "last_updated": datetime.now().isoformat(),
        "version": version,
        "flows": {
            k: {
                "title": v.get("title"),
                "description": v.get("description"),
                "nodes": v.get("nodes", []),
                "edges": v.get("edges", [])
            }
            for k, v in flows.items()
            if not v.get("error")
        },
        "diff_history": diff_history
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)

    print(f"  Diagram saved → v{version}")
    return saved