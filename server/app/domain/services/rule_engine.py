import random
import logging
from app.domain.entities.character import Character
from app.domain.entities.event import Event

logger = logging.getLogger(__name__)


class RuleEngine:
    """规则引擎：基于角色状态和条件判定事件触发"""

    def evaluate_events(
        self,
        character: Character,
        candidate_events: list[Event],
        max_events: int = 3,
    ) -> list[Event]:
        triggered = []
        for event in candidate_events:
            if self._check_conditions(event.trigger_condition, character):
                if random.random() < event.probability:
                    triggered.append(event)
                    logger.info(
                        "Event triggered: %s for character %s (age %d)",
                        event.title,
                        character.name,
                        character.age,
                    )

        prioritized = self._prioritize(triggered)
        return prioritized[:max_events]

    def _check_conditions(self, conditions: dict, character: Character) -> bool:
        if not conditions:
            return True

        if "min_age" in conditions and character.age < conditions["min_age"]:
            return False
        if "max_age" in conditions and character.age > conditions["max_age"]:
            return False

        stat_conditions = conditions.get("stats", {})
        for stat_name, threshold in stat_conditions.items():
            if hasattr(character.stats, stat_name):
                if getattr(character.stats, stat_name) < threshold:
                    return False

        required_stage = conditions.get("stage")
        if required_stage and character.stage.value != required_stage:
            return False

        return True

    def _prioritize(self, events: list[Event]) -> list[Event]:
        stage_events = [e for e in events if e.category == "milestone"]
        chain_events = [e for e in events if e.category == "chain"]
        random_events = [e for e in events if e.category not in ("milestone", "chain")]

        random.shuffle(stage_events)
        random.shuffle(chain_events)
        random.shuffle(random_events)

        return stage_events + chain_events + random_events

    def calculate_natural_stat_changes(self, character: Character) -> dict:
        """计算每年属性自然变化"""
        changes: dict[str, int] = {}
        age = character.age
        stats = character.stats

        # 健康变化
        if age < 20:
            changes["health"] = random.randint(0, 2)
        elif age < 40:
            changes["health"] = random.randint(-1, 1)
        elif age < 60:
            changes["health"] = random.randint(-2, 0)
        else:
            changes["health"] = random.randint(-3, -1)

        # 智力变化
        if age < 25:
            changes["intelligence"] = random.randint(1, 3)
        elif age < 60:
            changes["intelligence"] = random.randint(-1, 1)
        else:
            changes["intelligence"] = random.randint(-1, 0)

        # 魅力变化
        if age < 30:
            changes["charisma"] = random.randint(0, 2)
        elif age < 50:
            changes["charisma"] = random.randint(-1, 1)
        else:
            changes["charisma"] = random.randint(-2, -1)

        # 财富变化
        if 25 <= age <= 55:
            changes["wealth"] = random.randint(0, 3)
        else:
            changes["wealth"] = random.randint(-2, 1)

        # 幸福变化
        changes["happiness"] = random.randint(-3, 3)

        # 运气变化
        changes["luck"] = random.randint(-5, 5)

        return changes
