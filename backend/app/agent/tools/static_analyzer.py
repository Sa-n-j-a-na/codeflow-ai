import ast
import os

API_DECORATORS = {
    "get",
    "post",
    "put",
    "delete",
    "patch"
}


def analyze_codebase(codebase_path):
    result = {
        "apis": [],
        "services": [],
        "models": [],
        "dependencies": []
    }

    for root, _, files in os.walk(codebase_path):
        for file in files:

            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)

            try:
                with open(
                    filepath,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:
                    tree = ast.parse(f.read())

                analyze_ast(tree, file, result)

            except Exception:
                continue

    return result


def analyze_ast(tree, filename, result):

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):

            name = node.name

            if "service" in name.lower():
                result["services"].append(name)

            if (
                "model" in name.lower()
                or "entity" in name.lower()
            ):
                result["models"].append(name)

        elif isinstance(node, ast.FunctionDef):

            for deco in node.decorator_list:

                if isinstance(deco, ast.Call):

                    if isinstance(deco.func, ast.Attribute):

                        if deco.func.attr in API_DECORATORS:

                            result["apis"].append({
                                "endpoint": node.name,
                                "method": deco.func.attr.upper()
                            })

        elif isinstance(node, ast.ImportFrom):

            result["dependencies"].append(
                {
                    "file": filename,
                    "module": node.module
                }
            )