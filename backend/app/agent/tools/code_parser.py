import os
from pathlib import Path

def parse_structure(codebase_path: str) -> str:
    """
    Extracts high level structure from codebase.
    Lists all files with their size and type.
    This gives AI a map before reading full code.
    """
    structure_lines = []
    structure_lines.append("CODEBASE STRUCTURE MAP")
    structure_lines.append("=" * 50)

    IGNORE_DIRS = [
        "node_modules", ".git", "__pycache__",
        "venv", ".venv", "dist", "build"
    ]

    file_count = 0
    folder_count = 0

    for root, dirs, files in os.walk(codebase_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        # Show folder
        level = root.replace(codebase_path, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root)
        structure_lines.append(f"{indent}📁 {folder_name}/")
        folder_count += 1

        # Show files in folder
        for file in sorted(files):
            ext = Path(file).suffix.lower()
            file_path = os.path.join(root, file)

            try:
                size = os.path.getsize(file_path)
                size_str = f"{size:,} bytes"
            except:
                size_str = "unknown"

            sub_indent = "  " * (level + 1)
            structure_lines.append(
                f"{sub_indent}📄 {file} ({size_str})"
            )
            file_count += 1

    structure_lines.append("=" * 50)
    structure_lines.append(
        f"TOTAL: {file_count} files in {folder_count} folders"
    )

    return "\n".join(structure_lines)