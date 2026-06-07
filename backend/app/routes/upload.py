from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os
import zipfile

router = APIRouter()

# Temp folder to store uploads
UPLOAD_DIR = "/tmp/codeflow/uploads"

@router.post("/upload")
async def upload_codebase(
    file: UploadFile = File(...),
    flow_type: str = Form(default="system_flow")
):
    # Step 1 — Validate file type
    if not file.filename.endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only .zip files are supported"
        )

    try:
        # Step 2 — Create upload directory
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Step 3 — Save zip file
        zip_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Step 4 — Extract zip
        extract_path = os.path.join(UPLOAD_DIR, "extracted")
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)  # clear old extraction

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)

        return {
            "status": "success",
            "message": "Codebase uploaded and extracted",
            "path": extract_path,
            "flow_type": flow_type,
            "filename": file.filename
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )