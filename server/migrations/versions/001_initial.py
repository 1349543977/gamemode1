"""initial schema - create all 11 tables

Revision ID: 001_initial
Revises:
Create Date: 2026-06-04
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("openid", sa.String(128), nullable=False),
        sa.Column("union_id", sa.String(128), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("nickname", sa.String(50), nullable=False),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("platform", sa.String(20), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("openid"),
        sa.UniqueConstraint("union_id"),
        sa.UniqueConstraint("phone"),
    )
    op.create_index("ix_users_openid", "users", ["openid"])

    # 2. cities
    op.create_table(
        "cities",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("region", sa.String(50), nullable=False),
        sa.Column("population", sa.Integer(), nullable=False),
        sa.Column("development_index", sa.Float(), nullable=False),
        sa.Column("cost_of_living", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # 3. characters
    op.create_table(
        "characters",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("gender", sa.Enum("male", "female"), nullable=False),
        sa.Column("birth_year", sa.Integer(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("stage", sa.String(20), nullable=False),
        sa.Column("is_alive", sa.Boolean(), nullable=False),
        sa.Column("city_id", sa.BigInteger(), nullable=False),
        sa.Column("lifespan", sa.Integer(), nullable=False),
        sa.Column("death_cause", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
    )
    op.create_index("ix_characters_user_id", "characters", ["user_id"])

    # 4. character_stats
    op.create_table(
        "character_stats",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("character_id", sa.BigInteger(), nullable=False),
        sa.Column("health", sa.Integer(), nullable=False),
        sa.Column("intelligence", sa.Integer(), nullable=False),
        sa.Column("charisma", sa.Integer(), nullable=False),
        sa.Column("wealth", sa.Integer(), nullable=False),
        sa.Column("happiness", sa.Integer(), nullable=False),
        sa.Column("luck", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
        sa.UniqueConstraint("character_id"),
    )

    # 5. life_records
    op.create_table(
        "life_records",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("character_id", sa.BigInteger(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("stat_changes", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
    )
    op.create_index("idx_life_records_character_age", "life_records", ["character_id", "age"])

    # 6. events
    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("stage", sa.String(20), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("trigger_condition", sa.JSON(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_events_stage_category", "events", ["stage", "category"])

    # 7. event_results
    op.create_table(
        "event_results",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("choice_text", sa.String(200), nullable=False),
        sa.Column("choice_index", sa.Integer(), nullable=False),
        sa.Column("effects", sa.JSON(), nullable=False),
        sa.Column("narrative", sa.Text(), nullable=False),
        sa.Column("next_event_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["next_event_id"], ["events.id"]),
    )
    op.create_index("ix_event_results_event_id", "event_results", ["event_id"])

    # 8. relationships
    op.create_table(
        "relationships",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("character_id", sa.BigInteger(), nullable=False),
        sa.Column("target_name", sa.String(50), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("intimacy", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
    )
    op.create_index("ix_relationships_character_id", "relationships", ["character_id"])

    # 9. jobs
    op.create_table(
        "jobs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("min_intelligence", sa.Integer(), nullable=False),
        sa.Column("min_charisma", sa.Integer(), nullable=False),
        sa.Column("salary_range", sa.JSON(), nullable=False),
        sa.Column("stress_level", sa.Integer(), nullable=False),
        sa.Column("health_impact", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # 10. assets
    op.create_table(
        "assets",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("character_id", sa.BigInteger(), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("value", sa.DECIMAL(12, 2), nullable=False),
        sa.Column("acquired_age", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
    )

    # 11. world_states
    op.create_table(
        "world_states",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("era", sa.String(30), nullable=False),
        sa.Column("gdp_index", sa.Float(), nullable=False),
        sa.Column("tech_level", sa.Integer(), nullable=False),
        sa.Column("major_events", sa.JSON(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("year"),
    )
    op.create_index("ix_world_states_year", "world_states", ["year"])


def downgrade() -> None:
    op.drop_table("world_states")
    op.drop_table("assets")
    op.drop_table("jobs")
    op.drop_table("relationships")
    op.drop_table("event_results")
    op.drop_table("events")
    op.drop_table("life_records")
    op.drop_table("character_stats")
    op.drop_table("characters")
    op.drop_table("cities")
    op.drop_table("users")
