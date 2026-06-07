import time
from app.agent.tools.file_reader import read_codebase
from app.agent.tools.code_parser import parse_structure
from app.agent.tools.flow_builder import parse_ai_response, auto_layout
from app.agent.models.groq_model import call_ai_groq_only
from app.agent.models.gemini import call_gemini
from app.agent.prompts import PROMPT_MAP
from app.agent.architecture_store import (
    has_saved_diagram,
    load_saved_diagram,
    save_diagram
)
from app.agent.diff_engine import compare_flows


def build_groq_prompt(prompt_template, structure, content):
    instructions = prompt_template[:3_000]
    context = f"""
CODEBASE STRUCTURE:
{structure}

CODE SAMPLE:
{content[:8_000]}

[Codebase trimmed — use structure for complete picture]
"""
    return instructions + "\n\n" + context


def run_single_flow(prompt_template, structure, content, flow_type, is_first):
    if is_first:
        print(f"  [{flow_type}] Using Gemini...")
        prompt = prompt_template.replace("{structure}", structure)
        prompt = prompt.replace("{content}", content)
        raw = call_gemini(prompt)
        if not raw:
            print(f"  Gemini failed, using Groq...")
            raw = call_ai_groq_only(
                build_groq_prompt(prompt_template, structure, content)
            )
    else:
        print(f"  [{flow_type}] Using Groq...")
        raw = call_ai_groq_only(
            build_groq_prompt(prompt_template, structure, content)
        )

    if not raw:
        return {"error": f"All AI models failed for {flow_type}"}

    flow_data = parse_ai_response(raw)
    if "error" not in flow_data:
        flow_data = auto_layout(flow_data)
    return flow_data


def run_agent(codebase_path: str, flow_type: str = "all", source_url: str = None, force_refresh: bool = False) -> dict:
    print(f"\n{'='*50}")
    print(f"AGENT STARTING")
    print(f"{'='*50}")

    project_source = source_url or codebase_path
    is_refresh = force_refresh

    # KEY LOGIC — check if saved diagram exists
    saved = load_saved_diagram(project_source)

    if saved and not is_refresh:
        # Return saved diagram — no AI call needed
        print(f"\n  Found saved diagram v{saved.get('version')}")
        print(f"  Returning saved diagram — skipping AI analysis")
        return {
            "status": "success",
            "served_from_cache": True,
            "meta": {"files_analyzed": 0, "files_skipped": 0},
            "flows": saved.get("flows", {}),
            "diff": {
                "has_changes": False,
                "is_first_run": False,
                "served_from_cache": True,
                "last_analyzed": saved.get("last_updated", ""),
                "version": saved.get("version", 1)
            }
        }

    # No saved diagram OR refresh — run full analysis
    print("\n[1/4] Reading codebase...")
    codebase_data = read_codebase(codebase_path)
    if not codebase_data["content"]:
        return {"error": "No readable code files found"}
    print(f"Read {codebase_data['total_files']} files")

    print("\n[2/4] Parsing structure...")
    structure = parse_structure(codebase_path)

    print("\n[3/4] Generating flows...")
    results = {}
    flow_list = list(PROMPT_MAP.items())
    for i, (ft, prompt_template) in enumerate(flow_list):
        print(f"\n  → {ft} ({i+1}/3)...")
        results[ft] = run_single_flow(
            prompt_template, structure,
            codebase_data["content"], ft, is_first=(i == 0)
        )
        if i < len(flow_list) - 1:
            time.sleep(3)

    print("\n[4/4] Comparing and saving...")
    diff = compare_flows(saved, results)
    save_diagram(project_source, results, diff)

    for ft, data in results.items():
        if "error" in data:
            print(f"  ❌ {ft}: {data['error']}")
        else:
            print(f"  ✅ {ft}: {len(data.get('nodes',[]))} nodes")

    print("\nAGENT COMPLETE! ✅")
    return {
        "status": "success",
        "served_from_cache": False,
        "meta": {
            "files_analyzed": codebase_data["total_files"],
            "files_skipped": len(codebase_data["files_skipped"])
        },
        "flows": results,
        "diff": diff
    }