from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class LifeStage(str, Enum):
    INFANT = "infant"
    TODDLER = "toddler"
    CHILDHOOD = "childhood"
    ADOLESCENCE = "adolescence"
    YOUTH = "youth"
    PRIME = "prime"
    MIDDLE_AGE = "middle_age"
    ELDERLY = "elderly"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


STAGE_AGE_MAP = {
    LifeStage.INFANT: (0, 3),
    LifeStage.TODDLER: (4, 6),
    LifeStage.CHILDHOOD: (7, 12),
    LifeStage.ADOLESCENCE: (13, 18),
    LifeStage.YOUTH: (19, 30),
    LifeStage.PRIME: (31, 50),
    LifeStage.MIDDLE_AGE: (51, 65),
    LifeStage.ELDERLY: (66, 150),
}


@dataclass
class CharacterStats:
    health: int = 60
    intelligence: int = 50
    charisma: int = 50
    wealth: int = 30
    happiness: int = 60
    luck: int = 50

    def apply_effects(self, effects: dict) -> None:
        for attr, delta in effects.items():
            if hasattr(self, attr):
                current = getattr(self, attr)
                setattr(self, attr, max(0, min(100, current + delta)))

    def to_dict(self) -> dict:
        return {
            "health": self.health,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "wealth": self.wealth,
            "happiness": self.happiness,
            "luck": self.luck,
        }


@dataclass
class Character:
    id: Optional[int] = None
    user_id: int = 0
    name: str = ""
    gender: Gender = Gender.MALE
    birth_year: int = 2000
    age: int = 0
    stage: LifeStage = LifeStage.INFANT
    is_alive: bool = True
    city_id: int = 1
    lifespan: int = 75
    death_cause: Optional[str] = None
    stats: CharacterStats = field(default_factory=CharacterStats)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def advance_age(self) -> None:
        self.age += 1
        self._update_stage()

    def _update_stage(self) -> None:
        for stage, (min_age, max_age) in STAGE_AGE_MAP.items():
            if min_age <= self.age <= max_age:
                self.stage = stage
                break

    def calculate_effective_lifespan(self) -> int:
        health_modifier = (self.stats.health - 50) * 0.3
        wealth_modifier = (self.stats.wealth - 50) * 0.1
        return int(self.lifespan + health_modifier + wealth_modifier)

    def check_death(self) -> bool:
        if self.stats.health <= 0:
            self.is_alive = False
            self.death_cause = "健康耗尽"
            return True
        effective_lifespan = self.calculate_effective_lifespan()
        if self.age > effective_lifespan:
            import random
            death_probability = (self.age - effective_lifespan) * 0.1
            if random.random() < death_probability:
                self.is_alive = False
                self.death_cause = "自然衰老"
                return True
        return False
