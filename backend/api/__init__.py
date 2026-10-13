from fastapi import APIRouter
from backend.api import actions, health, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(actions.router, prefix="/api/actions", tags=["actions"])
api_router.include_router(ui.router, tags=["ui"])
