"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router as analysis_router
from .core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix=settings.api_v1_str)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Simple availability probe."""
    return {"status": "ok"}
