from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import git
import shutil
import os

router = APIRouter()

CLONE_DIR = "/tmp/codeflow/github"

# Pydantic model — validates incoming JSON
class GithubRequest(BaseModel):
    github_url: str
    flow_type: str = "system_flow"

@router.post("/github")
async def analyze_github(request: GithubRequest):

    # Step 1 — Basic URL validation
    if "github.com" not in request.github_url:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid GitHub URL"
        )

    try:
        # Step 2 — Clear old clone
        if os.path.exists(CLONE_DIR):
            shutil.rmtree(CLONE_DIR)
        os.makedirs(CLONE_DIR, exist_ok=True)

        # Step 3 — Clone the repo
        print(f"Cloning {request.github_url}...")
        git.Repo.clone_from(request.github_url, CLONE_DIR)
        print("Clone complete!")

        return {
            "status": "success",
            "message": "Repository cloned successfully",
            "path": CLONE_DIR,
            "flow_type": request.flow_type,
            "github_url": request.github_url
        }

    except git.exc.GitCommandError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Git clone failed — is the repo public? {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"GitHub analysis failed: {str(e)}"
        )