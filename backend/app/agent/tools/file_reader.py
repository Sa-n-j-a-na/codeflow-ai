import os
from pathlib import Path

# File types we care about
SUPPORTED_EXTENSIONS = [
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".go", ".rs", ".cpp", ".c",
    ".cs", ".php", ".rb", ".swift", ".kt",
    ".html", ".css", ".json", ".yaml", ".yml", ".md"
]

# Folders to skip completely
IGNORE_DIRS = [
    "node_modules", ".git", "__pycache__",
    ".venv", "venv", "dist", "build",
    ".next", ".idea", ".vscode", "coverage"
]

# Max characters to send to AI
# Gemini 2.5 Flash = 1M tokens ≈ 800K chars safe limit
MAX_CHARS = 800_000

def read_codebase(path: str) -> dict:
    """
    Walks a codebase directory and reads all source files.
    Returns a dict with content and metadata.
    """
    all_files = []
    all_content = []
    total_chars = 0
    skipped_files = []

    for root, dirs, files in os.walk(path):

        # Remove ignored directories in place
        # This stops os.walk from going into them
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in sorted(files):
            ext = Path(file).suffix.lower()

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, path)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Build file block
                file_block = f"\n\n{'='*50}\nFILE: {relative_path}\n{'='*50}\n{content}"

                # Check if adding this file exceeds limit
                if total_chars + len(file_block) > MAX_CHARS:
                    skipped_files.append(relative_path)
                    continue

                all_content.append(file_block)
                all_files.append(relative_path)
                total_chars += len(file_block)

            except Exception as e:
                skipped_files.append(f"{relative_path} (error: {e})")

    return {
        "content": "\n".join(all_content),
        "files_read": all_files,
        "files_skipped": skipped_files,
        "total_chars": total_chars,
        "total_files": len(all_files)
    }