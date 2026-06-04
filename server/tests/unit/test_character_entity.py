import pytest
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender


class TestCharacterStats:
    def test_apply_effects_positive(self):
        stats = CharacterStats(health=50, intelligence=50)
        stats.apply_effects({"health": 10, "intelligence": 5})
        assert stats.health == 60
        assert stats.intelligence == 55

    def test_apply_effects_negative(self):
        stats = CharacterStats(health=50)
        stats.apply_effects({"health": -20})
        assert stats.health == 30

    def test_apply_effects_clamp_min(self):
        stats = CharacterStats(health=10)
        stats.apply_effects({"health": -20})
        assert stats.health == 0

    def test_apply_effects_clamp_max(self):
        stats = CharacterStats(health=95)
        stats.apply_effects({"health": 20})
        assert stats.health == 100

    def test_to_dict(self):
        stats = CharacterStats()
        d = stats.to_dict()
        assert "health" in d
        assert "intelligence" in d
        assert len(d) == 6


class TestCharacter:
    def test_advance_age_infant(self):
        char = Character(age=0, stage=LifeStage.INFANT)
        char.advance_age()
        assert char.age == 1
        assert char.stage == LifeStage.INFANT

    def test_advance_age_stage_transition(self):
        char = Character(age=3, stage=LifeStage.INFANT)
        char.advance_age()
        assert char.age == 4
        assert char.stage == LifeStage.TODDLER

    def test_advance_age_to_adolescence(self):
        char = Character(age=12, stage=LifeStage.CHILDHOOD)
        char.advance_age()
        assert char.age == 13
        assert char.stage == LifeStage.ADOLESCENCE

    def test_check_death_health_zero(self):
        char = Character(stats=CharacterStats(health=0))
        assert char.check_death() is True
        assert char.is_alive is False
        assert char.death_cause == "健康耗尽"

    def test_check_death_health_positive(self):
        char = Character(age=20, stats=CharacterStats(health=80))
        assert char.check_death() is False
        assert char.is_alive is True

    def test_calculate_effective_lifespan(self):
        char = Character(lifespan=75, stats=CharacterStats(health=70, wealth=60))
        effective = char.calculate_effective_lifespan()
        assert effective == 75 + int((70 - 50) * 0.3) + int((60 - 50) * 0.1)
