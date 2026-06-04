import logging
from app.domain.entities.character import Character
from app.domain.entities.event import Event
from app.domain.interfaces.repository import IEventRepository
from app.domain.services.rule_engine import RuleEngine

logger = logging.getLogger(__name__)


class EventService:
    """事件服务：管理事件触发和选择处理"""

    def __init__(self, event_repo: IEventRepository, rule_engine: RuleEngine):
        self.event_repo = event_repo
        self.rule_engine = rule_engine

    async def get_pending_events(self, character: Character) -> list[Event]:
        """获取角色当前待处理的事件"""
        candidate_events = await self.event_repo.get_by_stage(character.stage.value)
        triggered = self.rule_engine.evaluate_events(character, candidate_events)

        for event in triggered:
            event.results = await self.event_repo.get_results(event.id)

        return triggered

    async def choose_event_option(
        self, event_id: int, choice_index: int, character: Character
    ) -> dict:
        """处理玩家的事件选择"""
        result = await self.event_repo.get_result_by_choice(event_id, choice_index)
        if not result:
            raise ValueError(f"Event {event_id} choice {choice_index} not found")

        character.stats.apply_effects(result.effects)

        triggered_events = []
        if result.next_event_id:
            next_event = await self.event_repo.get_by_id(result.next_event_id)
            if next_event:
                triggered_events.append(next_event)

        logger.info(
            "Character %s chose option %d for event %s",
            character.name,
            choice_index,
            event_id,
        )

        return {
            "narrative": result.narrative,
            "effects": result.effects,
            "new_stats": character.stats.to_dict(),
            "triggered_events": [
                {"id": e.id, "title": e.title, "description": e.description}
                for e in triggered_events
            ],
        }
