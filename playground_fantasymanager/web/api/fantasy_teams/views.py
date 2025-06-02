import secrets
from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Path, Query

from playground_fantasymanager.exceptions.base import ValidationError

from .schema import (
    ErrorResponse,
    FantasyTeam,
    FantasyTeamResponse,
    FantasyTeamUpdateRequest,
    PlayerInfo,
    TeamInfo,
)

router = APIRouter(prefix="/fTeams", tags=["Fantasy Teams"])


def random_team(match_id: str) -> FantasyTeam:
    """Generate a random fantasy team for a given match."""
    sysrand = secrets.SystemRandom()
    teams = [
        TeamInfo(
            team_id="t1",
            name="Chennai Super Kings",
            number_of_players=sysrand.randint(4, 7),
            team_image_url="https://example.com/csk.png",
        ),
        TeamInfo(
            team_id="t2",
            name="Mumbai Indians",
            number_of_players=sysrand.randint(4, 7),
            team_image_url="https://example.com/mi.png",
        ),
    ]
    players = [
        PlayerInfo(
            player_id=f"p{i}",
            player_name=sysrand.choice(["MS Dhoni", "Rohit Sharma", "Jasprit Bumrah"]),
            player_image_url="https://example.com/player.png",
            is_captain=(i == 1),
            is_vice_captain=(i == 2),
            credits=round(sysrand.uniform(8, 11), 1),
            points_earned=sysrand.randint(50, 150),
            position=sysrand.choice(["wk", "bat", "bowl", "allrounder"]),
            team_id=sysrand.choice(["t1", "t2"]),
        )
        for i in range(1, 12)
    ]
    return FantasyTeam(teams=teams, players=players)


@router.get(
    "/matches/{matchId}",
    response_model=FantasyTeamResponse,
    responses={400: {"model": ErrorResponse}},
)
async def get_default_fantasy_teams(
    match_id: str = Path(..., alias="matchId", description="Match ID"),
    fields: Optional[str] = Query(None, description="Comma-separated player fields"),
    limit: int = Query(2, ge=1, le=10),
    offset: int = Query(0, ge=0),
) -> FantasyTeamResponse:
    """Get default fantasy teams for a match."""
    if not match_id:
        raise ValidationError("matchId is required", description="Missing matchId")
    teams = [random_team(match_id) for _ in range(limit)]
    return FantasyTeamResponse(fantasy_teams=teams)


@router.get(
    "/user/{userId}/matches/{matchId}",
    response_model=FantasyTeamResponse,
    responses={400: {"model": ErrorResponse}},
)
async def get_user_fantasy_teams(
    user_id: str = Path(..., alias="userId", description="User ID"),
    match_id: str = Path(..., alias="matchId", description="Match ID"),
    fields: Optional[str] = Query(None, description="Comma-separated player fields"),
    limit: int = Query(2, ge=1, le=10),
    offset: int = Query(0, ge=0),
) -> FantasyTeamResponse:
    """Get fantasy teams for a user and match."""
    if not user_id or not match_id:
        raise ValidationError(
            "userId and matchId are required",
            description="Missing userId or matchId",
        )
    teams = [random_team(match_id) for _ in range(limit)]
    return FantasyTeamResponse(fantasy_teams=teams)


@router.get(
    "/user/{userId}/matches/{matchId}/fTeams/{fantasyTeamId}",
    response_model=FantasyTeam,
    responses={400: {"model": ErrorResponse}},
)
async def get_single_fantasy_team(
    user_id: str = Path(..., alias="userId", description="User ID"),
    match_id: str = Path(..., alias="matchId", description="Match ID"),
    fantasy_team_id: str = Path(
        ...,
        alias="fantasyTeamId",
        description="Fantasy Team ID",
    ),
    detail: bool = Query(True, description="Return detailed info"),
) -> FantasyTeam:
    """Get a single fantasy team for a user and match."""
    if not user_id or not match_id or not fantasy_team_id:
        raise ValidationError(
            "Missing required path parameters",
            description="userId, matchId, fantasyTeamId required",
        )
    return random_team(match_id)


@router.put(
    "/user/{userId}/matches/{matchId}/fTeams/{fantasyTeamId}/players",
    response_model=Dict[str, str],
    responses={400: {"model": ErrorResponse}},
)
async def update_fantasy_team_players(
    user_id: str = Path(..., alias="userId", description="User ID"),
    match_id: str = Path(..., alias="matchId", description="Match ID"),
    fantasy_team_id: str = Path(
        ...,
        alias="fantasyTeamId",
        description="Fantasy Team ID",
    ),
    players: List[FantasyTeamUpdateRequest] = Body(
        ...,
        description="List of player objects with updated positions",
    ),
) -> Dict[str, str]:
    """Update players in a fantasy team."""
    if not user_id or not match_id or not fantasy_team_id:
        raise ValidationError(
            "Missing required path parameters",
            description="userId, matchId, fantasyTeamId required",
        )
    return {"message": "Players updated successfully"}


@router.delete(
    "/user/{userId}/matches/{matchId}/fTeams/{fantasyTeamId}",
    response_model=Dict[str, str],
    responses={400: {"model": ErrorResponse}},
)
async def delete_fantasy_team(
    user_id: str = Path(..., alias="userId", description="User ID"),
    match_id: str = Path(..., alias="matchId", description="Match ID"),
    fantasy_team_id: str = Path(
        ...,
        alias="fantasyTeamId",
        description="Fantasy Team ID",
    ),
) -> Dict[str, str]:
    """Delete a fantasy team."""
    if not user_id or not match_id or not fantasy_team_id:
        raise ValidationError(
            "Missing required path parameters",
            description="userId, matchId, fantasyTeamId required",
        )
    return {"message": "Fantasy team deleted successfully"}
