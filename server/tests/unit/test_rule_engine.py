import pytest
from app.domain.services.rule_engine import RuleEngine
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender
from app.domain.entities.event import Event


class TestRuleEngine:
    def setup_method(self):
        self.engine = RuleEngine()
        self.character = Character(
            name="张三",
            gender=Gender.MALE,
            age=7,
            stage=LifeStage.CHILDHOOD,
            stats=CharacterStats(health=70, intelligence=60),
        )

    def test_evaluate_events_empty_candidates(self):
        result = self.engine.evaluate_events(self.character, [])
        assert result == []

    def test_evaluate_events_condition_pass(self):
        events = [
            Event(
                id=1, title="入学", stage="childhood", category="milestone",
                trigger_condition={"min_age": 7, "max_age": 7}, probability=1.0,
            ),
        ]
        result = self.engine.evaluate_events(self.character, events)
        assert len(result) == 1
        assert result[0].title == "入学"

    def test_evaluate_events_condition_fail_age(self):
        events = [
            Event(
                id=1, title="高考", stage="adolescence", category="milestone",
                trigger_condition={"min_age": 18, "max_age": 18}, probability=1.0,
            ),
        ]
        result = self.engine.evaluate_events(self.character, events)
        assert len(result) == 0

    def test_evaluate_events_condition_fail_stat(self):
        events = [
            Event(
                id=1, title="天才班", stage="childhood", category="milestone",
                trigger_condition={"stats": {"intelligence": 90}}, probability=1.0,
            ),
        ]
        result = self.engine.evaluate_events(self.character, events)
        assert len(result) == 0

    def test_evaluate_events_max_limit(self):
        events = [
            Event(id=i, title=f"Event {i}", stage="childhood", category="random",
                  trigger_condition={}, probability=1.0)
            for i in range(10)
        ]
        result = self.engine.evaluate_events(self.character, events, max_events=3)
        assert len(result) <= 3

    def test_calculate_natural_stat_changes_young(self):
        char = Character(age=10, stats=CharacterStats())
        changes = self.engine.calculate_natural_stat_changes(char)
        assert "health" in changes
        assert "intelligence" in changes
        assert changes["intelligence"] >= 1

    def test_calculate_natural_stat_changes_old(self):
        char = Character(age=70, stats=CharacterStats())
        changes = self.engine.calculate_natural_stat_changes(char)
        assert changes["health"] <= -1
