from fastapi import APIRouter

# APIRouter = mini app for grouping routes
router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "CodeFlow AI backend is running"
    }