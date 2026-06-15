def compare_architecture(old_saved: dict, new_architecture: dict):
    if not old_saved:
        return {
            "services_added": [],
            "services_removed": [],
            "models_added": [],
            "models_removed": [],
            "apis_added": [],
            "apis_removed": []
        }

    old_arch = old_saved.get("architecture_context", {})

    old_services = set(old_arch.get("services", []))
    new_services = set(new_architecture.get("services", []))

    old_models = set(old_arch.get("data_entities", []))
    new_models = set(new_architecture.get("data_entities", []))

    old_api_names = set()
    for api in old_arch.get("static_analysis", {}).get("apis", []):
        old_api_names.add(f"{api.get('method', '')}:{api.get('endpoint', '')}")

    new_api_names = set()
    for api in new_architecture.get("static_analysis", {}).get("apis", []):
        new_api_names.add(f"{api.get('method', '')}:{api.get('endpoint', '')}")

    return {
        "services_added":  sorted(list(new_services - old_services)),
        "services_removed": sorted(list(old_services - new_services)),
        "models_added":    sorted(list(new_models - old_models)),
        "models_removed":  sorted(list(old_models - new_models)),
        "apis_added":      sorted(list(new_api_names - old_api_names)),
        "apis_removed":    sorted(list(old_api_names - new_api_names))
    }


def compare_flows(
    old_saved: dict,
    new_flows: dict,
    architecture_context: dict = None
) -> dict:

    if not old_saved:
        return {
            "has_changes": False,
            "is_first_run": True
        }

    old_flow = old_saved.get("flows", {}).get("system_flow", {})
    new_flow = new_flows.get("system_flow", {})

    if not old_flow or not new_flow or new_flow.get("error"):
        return {
            "has_changes": False,
            "is_first_run": False
        }

    old_nodes = {n["id"]: n for n in old_flow.get("nodes", [])}
    new_nodes = {n["id"]: n for n in new_flow.get("nodes", [])}

    added_nodes = [
        {
            "label": n.get("label"),
            "type": n.get("type"),
            "technology": n.get("technology", "")
        }
        for nid, n in new_nodes.items()
        if nid not in old_nodes
    ]

    removed_nodes = [
        {
            "label": n.get("label"),
            "type": n.get("type")
        }
        for nid, n in old_nodes.items()
        if nid not in new_nodes
    ]

    changed_nodes = []
    for nid in set(old_nodes) & set(new_nodes):
        old = old_nodes[nid]
        new = new_nodes[nid]
        changes = []

        if old.get("label") != new.get("label"):
            changes.append(
                f"renamed: '{old.get('label')}' → '{new.get('label')}'"
            )

        if old.get("technology") != new.get("technology"):
            changes.append(
                f"tech changed: '{old.get('technology')}' → '{new.get('technology')}'"
            )

        if changes:
            changed_nodes.append({
                "label": new.get("label"),
                "changes": changes
            })

    architecture_diff = compare_architecture(
        old_saved,
        architecture_context or {}
    )

    architecture_changes = any([
        architecture_diff["services_added"],
        architecture_diff["services_removed"],
        architecture_diff["models_added"],
        architecture_diff["models_removed"],
        architecture_diff["apis_added"],
        architecture_diff["apis_removed"]
    ])

    has_changes = bool(
        added_nodes
        or removed_nodes
        or changed_nodes
        or architecture_changes
    )

    total = (
        len(added_nodes)
        + len(removed_nodes)
        + len(changed_nodes)
        + len(architecture_diff["services_added"])
        + len(architecture_diff["services_removed"])
        + len(architecture_diff["models_added"])
        + len(architecture_diff["models_removed"])
        + len(architecture_diff["apis_added"])
        + len(architecture_diff["apis_removed"])
    )

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
        },
        "architecture": architecture_diff
    }