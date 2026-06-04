from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.characters import router as characters_router
from app.api.v1.events import router as events_router
from app.api.v1.world import router as world_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(characters_router)
api_router.include_router(events_router)
api_router.include_router(world_router)
