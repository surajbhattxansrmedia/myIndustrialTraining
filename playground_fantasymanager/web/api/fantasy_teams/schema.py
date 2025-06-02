from typing import List, Optional

from pydantic import BaseModel


class TeamInfo(BaseModel):
    """Schema representing information about a team."""

    team_id: str
    name: str
    number_of_players: int
    team_image_url: Optional[str]


class PlayerInfo(BaseModel):
    """Schema representing information about a player."""

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
    """Request schema for updating a fantasy team."""

    player_id: str
    player_name: str
    player_image_url: Optional[str]
    is_captain: bool
    is_vice_captain: bool
    position: str
    team_id: str


class FantasyTeam(BaseModel):
    """Schema representing a fantasy team."""

    teams: List[TeamInfo]
    players: List[PlayerInfo]


class FantasyTeamResponse(BaseModel):
    """Response schema for a list of fantasy teams."""

    fantasy_teams: List[FantasyTeam]


class FantasyTeamFilteredFieldsResponse(BaseModel):
    """Response schema for filtered fantasy team fields."""

    fantasy_teams: List[FantasyTeam]  # Use List[Any] if truly dynamic
    count: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    status: int
    error: str
    code: str
    message: str
    description: str
