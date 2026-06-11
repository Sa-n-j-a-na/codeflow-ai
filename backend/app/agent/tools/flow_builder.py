import json
import re


def try_fix_truncated_json(raw: str) -> str:
    """
    Attempts to fix truncated JSON by closing
    open brackets and braces.
    """
    # Count open vs closed
    open_braces = raw.count('{') - raw.count('}')
    open_brackets = raw.count('[') - raw.count(']')

    fixed = raw.rstrip()

    # Remove trailing comma if present
    if fixed.endswith(','):
        fixed = fixed[:-1]

    # Close open structures
    fixed += ']' * open_brackets
    fixed += '}' * open_braces

    return fixed


def parse_ai_response(raw_response: str) -> dict:
    try:
        clean = re.sub(r"```json|```", "", raw_response).strip()
        return json.loads(clean)

    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        print("Attempting to fix truncated JSON...")

        try:
            fixed = try_fix_truncated_json(clean)
            result = json.loads(fixed)
            print("✅ JSON recovered successfully!")
            return result
        except Exception:
            print("❌ JSON recovery failed")
            return {
                "error": "AI returned invalid JSON",
                "raw_preview": raw_response[:500]
            }

    except Exception as e:
        return {"error": f"Parse failed: {str(e)}"}


def auto_layout(flow_data: dict) -> dict:
    nodes = flow_data.get("nodes", [])
    edges = flow_data.get("edges", [])

    if not nodes:
        return flow_data

    node_ids = [n["id"] for n in nodes]
    outgoing = {nid: [] for nid in node_ids}
    incoming = {nid: [] for nid in node_ids}

    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src in outgoing and tgt in incoming:
            outgoing[src].append(tgt)
            incoming[tgt].append(src)

    layers = {}
    queue = []

    for nid in node_ids:
        if len(incoming[nid]) == 0:
            layers[nid] = 0
            queue.append(nid)

    if not queue:
        layers[node_ids[0]] = 0
        queue.append(node_ids[0])

    visited = set(queue)
    while queue:
        current = queue.pop(0)
        for neighbor in outgoing[current]:
            if neighbor not in visited:
                layers[neighbor] = layers[current] + 1
                queue.append(neighbor)
                visited.add(neighbor)
            else:
                layers[neighbor] = max(
                    layers.get(neighbor, 0),
                    layers[current] + 1
                )

    for nid in node_ids:
        if nid not in layers:
            layers[nid] = 1

    layer_groups = {}
    for nid, layer in layers.items():
        layer_groups.setdefault(layer, []).append(nid)

    H_SPACING = 280
    V_SPACING = 180
    START_X = 150
    CANVAS_HEIGHT = 600

    node_positions = {}
    for layer_num in sorted(layer_groups.keys()):
        nodes_in_layer = layer_groups[layer_num]
        count = len(nodes_in_layer)
        x = START_X + layer_num * H_SPACING
        total_height = (count - 1) * V_SPACING
        start_y = max(80, (CANVAS_HEIGHT - total_height) // 2)

        for i, nid in enumerate(nodes_in_layer):
            node_positions[nid] = {
                "x": x,
                "y": start_y + i * V_SPACING
            }

    for node in nodes:
        node["position"] = node_positions.get(
            node["id"],
            {"x": START_X, "y": 300}
        )

    flow_data["nodes"] = nodes
    return flow_data