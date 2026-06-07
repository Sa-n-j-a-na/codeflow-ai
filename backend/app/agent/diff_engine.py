def compare_flows(old_saved: dict, new_flows: dict) -> dict:
    """
    Compares saved diagram with new analysis.
    Returns diff of what changed.
    """
    if not old_saved:
        return {"has_changes": False, "is_first_run": True}

    # Use system_flow as source of truth for diffing
    old_flow = old_saved.get("flows", {}).get("system_flow", {})
    new_flow = new_flows.get("system_flow", {})

    if not old_flow or not new_flow or new_flow.get("error"):
        return {"has_changes": False, "is_first_run": False}

    old_nodes = {n["id"]: n for n in old_flow.get("nodes", [])}
    new_nodes = {n["id"]: n for n in new_flow.get("nodes", [])}

    added_nodes = [
        {"label": n.get("label"), "type": n.get("type"), "technology": n.get("technology", "")}
        for nid, n in new_nodes.items() if nid not in old_nodes
    ]

    removed_nodes = [
        {"label": n.get("label"), "type": n.get("type")}
        for nid, n in old_nodes.items() if nid not in new_nodes
    ]

    changed_nodes = []
    for nid in set(old_nodes) & set(new_nodes):
        old = old_nodes[nid]
        new = new_nodes[nid]
        changes = []
        if old.get("label") != new.get("label"):
            changes.append(f"renamed: '{old.get('label')}' → '{new.get('label')}'")
        if old.get("technology") != new.get("technology"):
            changes.append(f"tech changed: '{old.get('technology')}' → '{new.get('technology')}'")
        if changes:
            changed_nodes.append({"label": new.get("label"), "changes": changes})

    has_changes = bool(added_nodes or removed_nodes or changed_nodes)
    total = len(added_nodes) + len(removed_nodes) + len(changed_nodes)

    return {
        "has_changes": has_changes,
        "is_first_run": False,
        "summary": f"{total} change(s) detected" if has_changes else "No changes detected",
        "version_from": old_saved.get("version", 1),
        "version_to": old_saved.get("version", 1) + 1,
        "last_analyzed": old_saved.get("last_updated", ""),
        "nodes": {
            "added": added_nodes,
            "removed": removed_nodes,
            "changed": changed_nodes
        }
    }