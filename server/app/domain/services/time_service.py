import logging
from app.domain.entities.character import Character
from app.domain.services.rule_engine import RuleEngine

logger = logging.getLogger(__name__)


class TimeService:
    """时间服务：管理角色年龄推进和阶段转换"""

    def __init__(self, rule_engine: RuleEngine):
        self.rule_engine = rule_engine

    def advance_year(self, character: Character) -> dict:
        """推进一年，返回年度变化摘要"""
        if not character.is_alive:
            raise ValueError(f"Character {character.name} is already dead")

        old_stage = character.stage
        character.advance_age()

        natural_changes = self.rule_engine.calculate_natural_stat_changes(character)
        character.stats.apply_effects(natural_changes)

        stage_changed = character.stage != old_stage

        died = character.check_death()

        logger.info(
            "Character %s advanced to age %d (stage: %s, alive: %s)",
            character.name,
            character.age,
            character.stage.value,
            character.is_alive,
        )

        return {
            "age": character.age,
            "stage": character.stage.value,
            "stage_changed": stage_changed,
            "natural_changes": natural_changes,
            "is_alive": character.is_alive,
            "death_cause": character.death_cause if died else None,
        }
