from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os
from routes.upload import router as upload_router
from routes.analyze import router as analyze_router
from routes.report import router as report_router
from routes.dashboard import router as dashboard_router

BACKEND_DIR = Path(__file__).resolve().parent
load_dotenv(BACKEND_DIR / ".env")


def _get_allowed_origins() -> list[str]:
    configured = os.getenv("CORS_ALLOW_ORIGINS", "").strip()
    if configured:
        parsed = [origin.strip().rstrip("/") for origin in configured.split(",") if origin.strip()]
        if parsed:
            return parsed

    return [
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://localhost:3000",
        "http://localhost:3001",
    ]


app = FastAPI(title="Expelexia Lab Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def root():
    return {"message": "Backend is running"}

# Register upload route
app.include_router(upload_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(report_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")