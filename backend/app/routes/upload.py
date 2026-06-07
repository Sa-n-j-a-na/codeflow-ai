from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.agent.agent_loop import run_agent
import shutil
import os
import zipfile

router = APIRouter()
UPLOAD_DIR = "/tmp/codeflow/uploads"

@router.post("/upload")
async def upload_codebase(
    file: UploadFile = File(...),
    flow_type: str = Form(default="system_flow")
):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files supported")

    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        zip_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(zip_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        extract_path = os.path.join(UPLOAD_DIR, "extracted")
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)

        # NOW call the agent
        result = run_agent(extract_path, flow_type)
        result["source_path"] = extract_path
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))