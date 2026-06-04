import logging
from app.domain.entities.character import Character
from app.domain.interfaces.repository import ICharacterRepository, IEventRepository
from app.domain.services.rule_engine import RuleEngine
from app.domain.services.time_service import TimeService
from app.domain.services.event_service import EventService

logger = logging.getLogger(__name__)


class GameEngine:
    """游戏引擎：协调时间推进、事件触发和状态更新"""

    def __init__(
        self,
        character_repo: ICharacterRepository,
        event_repo: IEventRepository,
        rule_engine: RuleEngine,
    ):
        self.character_repo = character_repo
        self.rule_engine = rule_engine
        self.time_service = TimeService(rule_engine)
        self.event_service = EventService(event_repo, rule_engine)

    async def advance_character(self, character_id: int) -> dict:
        """推进角色一年，返回完整年度结果"""
        character = await self.character_repo.get_by_id(character_id)
        if not character:
            raise ValueError(f"Character {character_id} not found")
        if not character.is_alive:
            raise ValueError(f"Character {character.name} is already dead")

        year_result = self.time_service.advance_year(character)

        pending_events = []
        if character.is_alive:
            pending_events = await self.event_service.get_pending_events(character)

        await self.character_repo.update(character)
        await self.character_repo.update_stats(character.id, character.stats)

        logger.info(
            "Advanced character %s to age %d, %d pending events",
            character.name,
            character.age,
            len(pending_events),
        )

        return {
            "character": {
                "age": character.age,
                "stage": character.stage.value,
                "is_alive": character.is_alive,
            },
            "year_summary": {
                "stat_changes": year_result["natural_changes"],
                "stage_changed": year_result["stage_changed"],
                "death_cause": year_result.get("death_cause"),
            },
            "pending_events": [
                {
                    "id": e.id,
                    "title": e.title,
                    "description": e.description,
                    "choices": [
                        {"index": r.choice_index, "text": r.choice_text}
                        for r in e.results
                    ],
                }
                for e in pending_events
            ],
        }
