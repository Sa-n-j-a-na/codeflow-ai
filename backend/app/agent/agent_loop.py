from app.agent.tools.file_reader import read_codebase
from app.agent.tools.code_parser import parse_structure
from app.agent.tools.flow_builder import parse_ai_response, auto_layout
from app.agent.models.groq_model import call_ai
from app.agent.prompts import PROMPT_MAP


def run_agent(codebase_path: str, flow_type: str = "system_flow") -> dict:
    """
    Main agent loop.
    Takes a codebase path and flow type.
    Returns complete flow diagram data.
    """

    print(f"\n{'='*50}")
    print(f"AGENT STARTING")
    print(f"Path: {codebase_path}")
    print(f"Flow Type: {flow_type}")
    print(f"{'='*50}")

    # STEP 1 — Read codebase
    print("\n[1/5] Reading codebase...")
    codebase_data = read_codebase(codebase_path)

    if not codebase_data["content"]:
        return {"error": "No readable code files found in this path"}

    print(f"Read {codebase_data['total_files']} files")
    print(f"Total size: {codebase_data['total_chars']:,} characters")

    # STEP 2 — Parse structure
    print("\n[2/5] Parsing codebase structure...")
    structure = parse_structure(codebase_path)
    print("Structure map built!")

    # STEP 3 — Build prompt
    print("\n[3/5] Building prompt...")
    prompt_template = PROMPT_MAP.get(flow_type, PROMPT_MAP["system_flow"])
    prompt = prompt_template.replace("{structure}", structure)
    prompt = prompt.replace("{content}", codebase_data["content"])
    print(f"Prompt size: {len(prompt):,} characters")

    # STEP 4 — Call AI
    print("\n[4/5] Calling AI model...")
    raw_response = call_ai(prompt)

    if not raw_response:
        return {"error": "All AI models failed to respond"}

    print("AI responded!")

    # STEP 5 — Parse and layout
    print("\n[5/5] Parsing response and building flow...")
    flow_data = parse_ai_response(raw_response)

    if "error" in flow_data:
        return flow_data

    flow_data = auto_layout(flow_data)

    # Add metadata
    flow_data["meta"] = {
        "files_analyzed": codebase_data["total_files"],
        "files_skipped": len(codebase_data["files_skipped"]),
        "flow_type": flow_type
    }

    print("\nAGENT COMPLETE! ✅")
    print(f"Nodes: {len(flow_data.get('nodes', []))}")
    print(f"Edges: {len(flow_data.get('edges', []))}")

    return flow_data