from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class RefreshRequest(BaseModel):
    path: str
    flow_type: str = "system_flow"

# Available flow types
FLOW_TYPES = [
    {
        "id": "system_flow",
        "label": "System Flow",
        "description": "Overall architecture and component relationships"
    },
    {
        "id": "api_flow",
        "label": "API Flow",
        "description": "Request and response flow through endpoints"
    },
    {
        "id": "data_flow",
        "label": "Data Flow",
        "description": "How data moves and transforms through the system"
    }
]

@router.post("/refresh")
async def refresh_flow(request: RefreshRequest):

    # Validate path exists
    if not os.path.exists(request.path):
        raise HTTPException(
            status_code=400,
            detail="Path not found — please upload or clone first"
        )

    return {
        "status": "success",
        "message": "Refresh triggered",
        "path": request.path,
        "flow_type": request.flow_type
    }

@router.get("/flow-types")
def get_flow_types():
    return {
        "flow_types": FLOW_TYPES
    }