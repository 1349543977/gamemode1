from pydantic import BaseModel, Field
from typing import Optional


class CreateCharacterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="角色姓名")
    gender: str = Field(..., pattern="^(male|female)$", description="性别")
    city_id: int = Field(..., gt=0, description="出生城市ID")


class CharacterStatsResponse(BaseModel):
    health: int
    intelligence: int
    charisma: int
    wealth: int
    happiness: int
    luck: int


class CityBrief(BaseModel):
    id: int
    name: str


class CharacterResponse(BaseModel):
    id: int
    name: str
    gender: str
    age: int
    stage: str
    is_alive: bool
    city: Optional[CityBrief] = None
    stats: Optional[CharacterStatsResponse] = None


class LifeRecordResponse(BaseModel):
    id: int
    age: int
    year: int
    summary: str
    stat_changes: Optional[dict] = None


class AdvanceYearResponse(BaseModel):
    character: dict
    year_summary: dict
    pending_events: list
