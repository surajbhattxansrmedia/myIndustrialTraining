from fastapi.routing import APIRouter

from playground_fantasymanager.web.api import echo, monitoring
from playground_fantasymanager.web.api.fantasy_teams.views import (
    router as fantasy_teams_router,
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])

api_router.include_router(fantasy_teams_router)
