from typing import List, Optional, Any
from pydantic import BaseModel


class TeamInfo(BaseModel):
    team_id: str
    name: str
    number_of_players: int
    team_image_url: Optional[str]


class PlayerInfo(BaseModel):
    player_id: str
    player_name: str
    player_image_url: Optional[str]
    is_captain: bool
    is_vice_captain: bool
    credits: Optional[float]
    points_earned: Optional[float]
    position: str
    team_id: str


class FantasyTeamUpdateRequest(BaseModel):
    player_id: str
    player_name: str
    player_image_url: Optional[str]
    is_captain: bool
    is_vice_captain: bool
    position: str
    team_id: str


class FantasyTeam(BaseModel):
    teams: List[TeamInfo]
    players: List[PlayerInfo]


class FantasyTeamResponse(BaseModel):
    fantasy_teams: List[FantasyTeam]


class FantasyTeamFilteredFieldsResponse(BaseModel):
    fantasy_teams: List[Any]
    count: int


class ErrorResponse(BaseModel):
    status: int
    error: str
    code: str
    message: str
    description: str
