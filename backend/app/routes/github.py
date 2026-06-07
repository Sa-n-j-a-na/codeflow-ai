from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.agent_loop import run_agent
import git
import shutil
import os
import tempfile
import traceback
import stat

router = APIRouter()

class GithubRequest(BaseModel):
    github_url: str
    flow_type: str = "system_flow"

def force_delete(path: str):
    """
    Force deletes a folder on Windows.
    Git repos have read-only files that block normal delete.
    This fixes permission before deleting.
    """
    def fix_permission(func, path, excinfo):
        # Remove read-only flag and retry
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(path):
        shutil.rmtree(path, onerror=fix_permission)
        print(f"Deleted: {path}")

@router.post("/github")
async def analyze_github(request: GithubRequest):
    if "github.com" not in request.github_url:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    clone_dir = os.path.join(tempfile.gettempdir(), "codeflow", "github")

    try:
        # Force delete with permission fix
        force_delete(clone_dir)

        # Fresh folder
        os.makedirs(clone_dir, exist_ok=True)
        print(f"Cloning {request.github_url}...")

        git.Repo.clone_from(request.github_url, clone_dir)
        print("Clone complete!")

        print("Starting agent...")
        result = run_agent(clone_dir, request.flow_type)
        result["source_path"] = clone_dir
        return result

    except git.exc.GitCommandError as e:
        raise HTTPException(status_code=400, detail=f"Clone failed: {str(e)}")
    except Exception as e:
        print("FULL ERROR:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))