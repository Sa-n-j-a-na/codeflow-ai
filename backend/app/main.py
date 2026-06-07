from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_NAME, APP_VERSION, FRONTEND_URL
from app.routes.health import router as health_router

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

# CORS — allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect routes
app.include_router(health_router, prefix="/api")

# Root route
@app.get("/")
def root():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }