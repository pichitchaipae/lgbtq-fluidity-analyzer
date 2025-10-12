"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .api.routes import router as analysis_router_v1
from .api.routes_v2 import router as analysis_router_v2, limiter
from .api.routes_chatbot import router as chatbot_router
from .core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis_router_v1, prefix=settings.api_v1_str)
app.include_router(analysis_router_v2, prefix="/api")
app.include_router(chatbot_router, prefix="/api")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Simple availability probe."""
    return {"status": "ok"}
