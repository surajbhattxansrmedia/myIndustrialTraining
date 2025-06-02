from fastapi import APIRouter, Query, Path, Body
from typing import Optional, List, Dict, Any
import random
from .schema import (
    FantasyTeamResponse,
    FantasyTeam,
    TeamInfo,
    PlayerInfo,
    FantasyTeamFilteredFieldsResponse,
    ErrorResponse,
    FantasyTeamUpdateRequest,
)
from playground_fantasymanager.exceptions.base import ValidationError

router = APIRouter(prefix="/fTeams", tags=["Fantasy Teams"])


def random_team(match_id: str) -> FantasyTeam:
    teams = [
        TeamInfo(
            team_id="t1",
            name="Chennai Super Kings",
            number_of_players=random.randint(4, 7),
            team_image_url="https://example.com/csk.png",
        ),
        TeamInfo(
            team_id="t2",
            name="Mumbai Indians",
            number_of_players=random.randint(4, 7),
            team_image_url="https://example.com/mi.png",
        ),
    ]
    players = [
        PlayerInfo(
            player_id=f"p{i}",
            player_name=random.choice(["MS Dhoni", "Rohit Sharma", "Jasprit Bumrah"]),
            player_image_url="https://example.com/player.png",
            is_captain=(i == 1),
            is_vice_captain=(i == 2),
            credits=round(random.uniform(8, 11), 1),
            points_earned=random.randint(50, 150),
            position=random.choice(["wk", "bat", "bowl", "allrounder"]),
            team_id=random.choice(["t1", "t2"]),
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
    matchId: str = Path(..., description="Match ID"),
    fields: Optional[str] = Query(None, description="Comma-separated player fields"),
    limit: int = Query(2, ge=1, le=10),
    offset: int = Query(0, ge=0),
):
    if not matchId:
        raise ValidationError("matchId is required", description="Missing matchId")
    teams = [random_team(matchId) for _ in range(limit)]
    return FantasyTeamResponse(fantasy_teams=teams)


@router.get(
    "/user/{userId}/matches/{matchId}",
    response_model=FantasyTeamResponse,
    responses={400: {"model": ErrorResponse}},
)
async def get_user_fantasy_teams(
    userId: str = Path(..., description="User ID"),
    matchId: str = Path(..., description="Match ID"),
    fields: Optional[str] = Query(None, description="Comma-separated player fields"),
    limit: int = Query(2, ge=1, le=10),
    offset: int = Query(0, ge=0),
):
    if not userId or not matchId:
        raise ValidationError(
            "userId and matchId are required", description="Missing userId or matchId"
        )
    teams = [random_team(matchId) for _ in range(limit)]
    return FantasyTeamResponse(fantasy_teams=teams)


@router.get(
    "/user/{userId}/matches/{matchId}/fTeams/{fantasyTeamId}",
    response_model=FantasyTeam,
    responses={400: {"model": ErrorResponse}},
)
async def get_single_fantasy_team(
    userId: str = Path(..., description="User ID"),
    matchId: str = Path(..., description="Match ID"),
    fantasyTeamId: str = Path(..., description="Fantasy Team ID"),
    detail: bool = Query(True, description="Return detailed info"),
):
    if not userId or not matchId or not fantasyTeamId:
        raise ValidationError(
            "Missing required path parameters",
            description="userId, matchId, fantasyTeamId required",
        )
    return random_team(matchId)


@router.put(
    "/user/{userId}/matches/{matchId}/fTeams/{fantasyTeamId}/players",
    response_model=Dict[str, str],
    responses={400: {"model": ErrorResponse}},
)
async def update_fantasy_team_players(
    userId: str = Path(..., description="User ID"),
    matchId: str = Path(..., description="Match ID"),
    fantasyTeamId: str = Path(..., description="Fantasy Team ID"),
    players: List[FantasyTeamUpdateRequest] = Body(
        ..., description="List of player objects with updated positions"
    ),
):
    if not userId or not matchId or not fantasyTeamId:
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
    userId: str = Path(..., description="User ID"),
    matchId: str = Path(..., description="Match ID"),
    fantasyTeamId: str = Path(..., description="Fantasy Team ID"),
):
    if not userId or not matchId or not fantasyTeamId:
        raise ValidationError(
            "Missing required path parameters",
            description="userId, matchId, fantasyTeamId required",
        )
    return {"message": "Fantasy team deleted successfully"}
