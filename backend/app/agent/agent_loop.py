import time
from app.agent.tools.file_reader import read_codebase
from app.agent.tools.code_parser import parse_structure
from app.agent.tools.flow_builder import parse_ai_response, auto_layout
from app.agent.models.groq_model import call_ai_groq_only
from app.agent.models.gemini import call_gemini
from app.agent.prompts import PROMPT_MAP

# Groq TPM limits are tiny — send structure only, not full code
# Structure map is ~5K chars = ~1.2K tokens = well within limits
GROQ_MAX_CHARS = 15_000


def build_groq_prompt(prompt_template: str, structure: str, content: str) -> str:
    """
    For Groq — use structure + first portion of code only.
    Groq TPM is too small for full codebase.
    """
    # Take prompt instructions only (first 3K chars)
    instructions = prompt_template[:3_000]

    # Use structure map + small code sample
    context = f"""
CODEBASE STRUCTURE:
{structure}

CODE SAMPLE (first files):
{content[:8_000]}

[Full codebase trimmed for model limits — use structure above for complete picture]
"""
    full_prompt = instructions + "\n\n" + context

    print(f"  Groq prompt size: {len(full_prompt):,} chars (~{len(full_prompt)//4:,} tokens)")
    return full_prompt


def run_single_flow(
    prompt_template: str,
    structure: str,
    content: str,
    flow_type: str,
    is_first: bool
) -> dict:

    if is_first:
        # First flow — use full prompt with Gemini
        print(f"  [{flow_type}] Using Gemini (full codebase)...")
        prompt = prompt_template.replace("{structure}", structure)
        prompt = prompt.replace("{content}", content)
        raw_response = call_gemini(prompt)

        if not raw_response:
            print(f"  Gemini failed, trying Groq with trimmed prompt...")
            prompt = build_groq_prompt(prompt_template, structure, content)
            raw_response = call_ai_groq_only(prompt)
    else:
        # Other flows — use trimmed prompt with Groq
        print(f"  [{flow_type}] Using Groq (structure-only prompt)...")
        prompt = build_groq_prompt(prompt_template, structure, content)
        raw_response = call_ai_groq_only(prompt)

    if not raw_response:
        return {"error": f"All AI models failed for {flow_type}"}

    flow_data = parse_ai_response(raw_response)
    if "error" not in flow_data:
        flow_data = auto_layout(flow_data)

    return flow_data


def run_agent(codebase_path: str, flow_type: str = "all") -> dict:
    print(f"\n{'='*50}")
    print(f"AGENT STARTING")
    print(f"Path: {codebase_path}")
    print(f"{'='*50}")

    print("\n[1/4] Reading codebase...")
    codebase_data = read_codebase(codebase_path)

    if not codebase_data["content"]:
        return {"error": "No readable code files found"}

    print(f"Read {codebase_data['total_files']} files — {codebase_data['total_chars']:,} chars")

    print("\n[2/4] Parsing structure...")
    structure = parse_structure(codebase_path)
    print(f"Structure size: {len(structure):,} chars")

    print("\n[3/4] Generating flows...")
    results = {}
    flow_list = list(PROMPT_MAP.items())

    for i, (ft, prompt_template) in enumerate(flow_list):
        print(f"\n  → {ft} ({i+1}/3)...")
        results[ft] = run_single_flow(
            prompt_template,
            structure,
            codebase_data["content"],
            ft,
            is_first=(i == 0)
        )
        if i < len(flow_list) - 1:
            time.sleep(3)

    print("\n[4/4] Done!")
    final = {
        "status": "success",
        "meta": {
            "files_analyzed": codebase_data["total_files"],
            "files_skipped": len(codebase_data["files_skipped"]),
        },
        "flows": results
    }

    for ft, data in results.items():
        if "error" in data:
            print(f"  ❌ {ft}: {data['error']}")
        else:
            print(f"  ✅ {ft}: {len(data.get('nodes',[]))} nodes, {len(data.get('edges',[]))} edges")

    print("\nAGENT COMPLETE! ✅")
    return final