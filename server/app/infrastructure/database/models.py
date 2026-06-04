from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    Text, DateTime, JSON, Enum, DECIMAL, ForeignKey, Index,
)
from sqlalchemy.orm import relationship
from app.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(128), unique=True, nullable=False, index=True)
    union_id = Column(String(128), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    nickname = Column(String(50), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    platform = Column(String(20), nullable=False)
    last_login_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    characters = relationship("CharacterModel", back_populates="user")


class CharacterModel(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum("male", "female"), nullable=False)
    birth_year = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    stage = Column(String(20), nullable=False, default="infant")
    is_alive = Column(Boolean, nullable=False, default=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    lifespan = Column(Integer, nullable=False, default=75)
    death_cause = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="characters")
    stats = relationship("CharacterStatsModel", back_populates="character", uselist=False)
    life_records = relationship("LifeRecordModel", back_populates="character")
    relationships_rel = relationship("RelationshipModel", back_populates="character")
    assets = relationship("AssetModel", back_populates="character")
    city = relationship("CityModel")


class CharacterStatsModel(Base):
    __tablename__ = "character_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"), unique=True, nullable=False)
    health = Column(Integer, nullable=False, default=60)
    intelligence = Column(Integer, nullable=False, default=50)
    charisma = Column(Integer, nullable=False, default=50)
    wealth = Column(Integer, nullable=False, default=30)
    happiness = Column(Integer, nullable=False, default=60)
    luck = Column(Integer, nullable=False, default=50)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    character = relationship("CharacterModel", back_populates="stats")


class LifeRecordModel(Base):
    __tablename__ = "life_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    age = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    summary = Column(Text, nullable=False)
    stat_changes = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    character = relationship("CharacterModel", back_populates="life_records")

    __table_args__ = (
        Index("idx_life_records_character_age", "character_id", "age"),
    )


class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    stage = Column(String(20), nullable=False)
    category = Column(String(30), nullable=False)
    trigger_condition = Column(JSON, nullable=False)
    probability = Column(Float, nullable=False, default=1.0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    results = relationship("EventResultModel", back_populates="event", foreign_keys="EventResultModel.event_id")

    __table_args__ = (
        Index("idx_events_stage_category", "stage", "category"),
    )


class EventResultModel(Base):
    __tablename__ = "event_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    choice_text = Column(String(200), nullable=False)
    choice_index = Column(Integer, nullable=False)
    effects = Column(JSON, nullable=False)
    narrative = Column(Text, nullable=False)
    next_event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    event = relationship("EventModel", back_populates="results", foreign_keys=[event_id])


class RelationshipModel(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    target_name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    intimacy = Column(Integer, nullable=False, default=50)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    character = relationship("CharacterModel", back_populates="relationships_rel")


class CityModel(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    population = Column(Integer, nullable=False)
    development_index = Column(Float, nullable=False)
    cost_of_living = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    category = Column(String(30), nullable=False)
    min_intelligence = Column(Integer, nullable=False, default=0)
    min_charisma = Column(Integer, nullable=False, default=0)
    salary_range = Column(JSON, nullable=False)
    stress_level = Column(Integer, nullable=False, default=50)
    health_impact = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AssetModel(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    type = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(DECIMAL(12, 2), nullable=False)
    acquired_age = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    character = relationship("CharacterModel", back_populates="assets")


class WorldStateModel(Base):
    __tablename__ = "world_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, unique=True, nullable=False, index=True)
    era = Column(String(30), nullable=False)
    gdp_index = Column(Float, nullable=False)
    tech_level = Column(Integer, nullable=False)
    major_events = Column(JSON, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
