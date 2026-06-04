from pydantic import BaseModel
from typing import Optional


class CityResponse(BaseModel):
    id: int
    name: str
    region: str
    population: int
    development_index: float
    cost_of_living: float


class JobResponse(BaseModel):
    id: int
    name: str
    category: str
    min_intelligence: int
    min_charisma: int
    salary_range: dict
    stress_level: int
    health_impact: int


class WorldStateResponse(BaseModel):
    year: int
    era: str
    gdp_index: float
    tech_level: int
    major_events: Optional[list] = None
