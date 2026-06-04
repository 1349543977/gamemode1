import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.services.game_engine import GameEngine
from app.domain.services.rule_engine import RuleEngine
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender


class TestGameEngine:
    def setup_method(self):
        self.character_repo = AsyncMock()
        self.event_repo = AsyncMock()
        self.rule_engine = RuleEngine()
        self.engine = GameEngine(
            self.character_repo, self.event_repo, self.rule_engine
        )

    @pytest.mark.asyncio
    async def test_advance_character_success(self):
        character = Character(
            id=1, name="张三", gender=Gender.MALE, age=6,
            stage=LifeStage.TODDLER, stats=CharacterStats(health=80, intelligence=60),
        )
        self.character_repo.get_by_id = AsyncMock(return_value=character)
        self.character_repo.update = AsyncMock(return_value=character)
        self.character_repo.update_stats = AsyncMock(return_value=character.stats)
        self.event_repo.get_by_stage = AsyncMock(return_value=[])

        result = await self.engine.advance_character(1)

        assert result["character"]["age"] == 7
        assert result["character"]["stage"] == "childhood"
        assert "year_summary" in result
        assert "pending_events" in result

    @pytest.mark.asyncio
    async def test_advance_character_not_found(self):
        self.character_repo.get_by_id = AsyncMock(return_value=None)

        with pytest.raises(ValueError, match="not found"):
            await self.engine.advance_character(999)

    @pytest.mark.asyncio
    async def test_advance_character_dead(self):
        character = Character(id=1, name="张三", is_alive=False, death_cause="衰老")
        self.character_repo.get_by_id = AsyncMock(return_value=character)

        with pytest.raises(ValueError, match="already dead"):
            await self.engine.advance_character(1)
