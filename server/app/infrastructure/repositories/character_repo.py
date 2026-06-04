from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender
from app.domain.interfaces.repository import ICharacterRepository
from app.infrastructure.database.models import CharacterModel, CharacterStatsModel


class CharacterRepository(ICharacterRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_id(self, character_id: int) -> Optional[Character]:
        model = self.db.query(CharacterModel).filter(CharacterModel.id == character_id).first()
        if not model:
            return None
        return self._to_entity(model)

    async def get_by_user_id(self, user_id: int) -> list[Character]:
        models = self.db.query(CharacterModel).filter(CharacterModel.user_id == user_id).all()
        return [self._to_entity(m) for m in models]

    async def create(self, character: Character) -> Character:
        model = CharacterModel(
            user_id=character.user_id,
            name=character.name,
            gender=character.gender.value,
            birth_year=character.birth_year,
            age=character.age,
            stage=character.stage.value,
            is_alive=character.is_alive,
            city_id=character.city_id,
            lifespan=character.lifespan,
        )
        self.db.add(model)
        self.db.flush()

        stats_model = CharacterStatsModel(
            character_id=model.id,
            health=character.stats.health,
            intelligence=character.stats.intelligence,
            charisma=character.stats.charisma,
            wealth=character.stats.wealth,
            happiness=character.stats.happiness,
            luck=character.stats.luck,
        )
        self.db.add(stats_model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def update(self, character: Character) -> Character:
        model = self.db.query(CharacterModel).filter(CharacterModel.id == character.id).first()
        if not model:
            raise ValueError(f"Character {character.id} not found")
        model.age = character.age
        model.stage = character.stage.value
        model.is_alive = character.is_alive
        model.lifespan = character.lifespan
        model.death_cause = character.death_cause
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def get_stats(self, character_id: int) -> Optional[CharacterStats]:
        model = self.db.query(CharacterStatsModel).filter(
            CharacterStatsModel.character_id == character_id
        ).first()
        if not model:
            return None
        return CharacterStats(
            health=model.health,
            intelligence=model.intelligence,
            charisma=model.charisma,
            wealth=model.wealth,
            happiness=model.happiness,
            luck=model.luck,
        )

    async def update_stats(self, character_id: int, stats: CharacterStats) -> CharacterStats:
        model = self.db.query(CharacterStatsModel).filter(
            CharacterStatsModel.character_id == character_id
        ).first()
        if not model:
            raise ValueError(f"Stats for character {character_id} not found")
        model.health = stats.health
        model.intelligence = stats.intelligence
        model.charisma = stats.charisma
        model.wealth = stats.wealth
        model.happiness = stats.happiness
        model.luck = stats.luck
        self.db.commit()
        return stats

    @staticmethod
    def _to_entity(model: CharacterModel) -> Character:
        stats = CharacterStats()
        if model.stats:
            stats = CharacterStats(
                health=model.stats.health,
                intelligence=model.stats.intelligence,
                charisma=model.stats.charisma,
                wealth=model.stats.wealth,
                happiness=model.stats.happiness,
                luck=model.stats.luck,
            )
        return Character(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            gender=Gender(model.gender),
            birth_year=model.birth_year,
            age=model.age,
            stage=LifeStage(model.stage),
            is_alive=model.is_alive,
            city_id=model.city_id,
            lifespan=model.lifespan,
            death_cause=model.death_cause,
            stats=stats,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
