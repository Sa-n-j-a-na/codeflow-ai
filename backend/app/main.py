from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import APP_NAME, APP_VERSION, FRONTEND_URL
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.github import router as github_router
from app.routes.flows import router as flows_router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All routes
app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(github_router, prefix="/api")
app.include_router(flows_router, prefix="/api")

@app.get("/")
def root():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }