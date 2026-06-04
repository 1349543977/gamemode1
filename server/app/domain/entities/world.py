from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class City:
    id: Optional[int] = None
    name: str = ""
    region: str = ""
    population: int = 0
    development_index: float = 0.5
    cost_of_living: float = 0.5


@dataclass
class Job:
    id: Optional[int] = None
    name: str = ""
    category: str = ""
    min_intelligence: int = 0
    min_charisma: int = 0
    salary_range: dict = field(default_factory=lambda: {"min": 3000, "max": 8000})
    stress_level: int = 50
    health_impact: int = 0


@dataclass
class WorldState:
    id: Optional[int] = None
    year: int = 2000
    era: str = ""
    gdp_index: float = 0.5
    tech_level: int = 5
    major_events: list = field(default_factory=list)
    updated_at: datetime = field(default_factory=datetime.utcnow)
