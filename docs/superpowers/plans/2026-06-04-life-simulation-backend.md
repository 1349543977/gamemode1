# 虚拟现实人生养成游戏 - 后端 MVP 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建人生养成游戏后端MVP，包含认证、角色管理、时间推进、事件系统和规则引擎。

**Architecture:** FastAPI + Clean Architecture，领域层不依赖框架，Repository Pattern隔离数据访问，规则引擎驱动事件生成，JWT认证。

**Tech Stack:** Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic, Redis, Celery, MySQL 8.0, Pydantic v2, Docker

---

## 文件结构映射

```
server/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI应用入口
│   ├── config.py                        # pydantic-settings配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                      # 依赖注入
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py                # v1路由聚合
│   │       ├── auth.py                  # 认证API
│   │       ├── characters.py            # 角色API
│   │       ├── events.py                # 事件API
│   │       └── world.py                 # 世界API
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                  # 用户领域实体
│   │   │   ├── character.py             # 角色领域实体
│   │   │   ├── event.py                 # 事件领域实体
│   │   │   └── world.py                 # 世界领域实体
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── game_engine.py           # 游戏引擎（核心）
│   │   │   ├── rule_engine.py           # 规则引擎
│   │   │   ├── time_service.py          # 时间服务
│   │   │   └── event_service.py         # 事件服务
│   │   └── interfaces/
│   │       ├── __init__.py
│   │       └── repository.py            # Repository抽象接口
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py            # 数据库连接
│   │   │   └── models.py               # SQLAlchemy ORM模型
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repo.py
│   │   │   ├── character_repo.py
│   │   │   └── event_repo.py
│   │   ├── cache/
│   │   │   ├── __init__.py
│   │   │   └── redis_client.py
│   │   └── tasks/
│   │       ├── __init__.py
│   │       └── game_tasks.py
│   └── schemas/
│       ├── __init__.py
│       ├── auth.py
│       ├── character.py
│       ├── event.py
│       └── world.py
├── migrations/
│   ├── env.py
│   └── versions/
│       └── 001_initial.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_rule_engine.py
│   │   ├── test_game_engine.py
│   │   ├── test_time_service.py
│   │   └── test_event_service.py
│   └── integration/
│       ├── __init__.py
│       ├── test_auth_api.py
│       ├── test_character_api.py
│       └── test_event_api.py
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

### Task 1: 项目初始化与基础设施

**Files:**
- Create: `server/requirements.txt`
- Create: `server/.env.example`
- Create: `server/.gitignore`
- Create: `server/app/__init__.py`
- Create: `server/app/config.py`
- Create: `server/app/main.py`
- Create: `server/Dockerfile`
- Create: `server/docker-compose.yml`

- [ ] **Step 1: 创建项目目录和requirements.txt**

```txt
# Web Framework
fastapi==0.111.0
uvicorn[standard]==0.30.1

# Database
sqlalchemy==2.0.31
alembic==1.13.1
pymysql==1.1.1
cryptography==42.0.8

# Redis
redis==5.0.7

# Task Queue
celery==5.4.0

# Auth
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Validation
pydantic==2.7.4
pydantic-settings==2.3.4

# HTTP Client (for WeChat API)
httpx==0.27.0

# Testing
pytest==8.2.2
pytest-asyncio==0.23.7
httpx==0.27.0

# Logging
structlog==24.2.0

# CORS
python-multipart==0.0.9
```

- [ ] **Step 2: 创建环境配置文件**

`.env.example`:
```env
# Application
APP_NAME=LifeSimulation
APP_ENV=development
DEBUG=true
SECRET_KEY=change-me-in-production
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/life_sim
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# WeChat
WECHAT_APP_ID=your-app-id
WECHAT_APP_SECRET=your-app-secret

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

- [ ] **Step 3: 创建.gitignore**

```gitignore
__pycache__/
*.py[cod]
*.egg-info/
dist/
.env
.venv/
venv/
*.db
.pytest_cache/
.mypy_cache/
htmlcov/
```

- [ ] **Step 4: 创建配置模块**

`server/app/config.py`:
```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "LifeSimulation"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-in-production"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "mysql+pymysql://root:password@localhost:3306/life_sim"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440
    jwt_refresh_token_expire_days: int = 30

    wechat_app_id: str = ""
    wechat_app_secret: str = ""

    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 5: 创建FastAPI入口**

`server/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.v1.router import api_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url=f"{settings.api_v1_prefix}/docs",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health_check():
    return {"status": "ok", "env": settings.app_env}
```

- [ ] **Step 6: 创建占位路由文件**

`server/app/api/__init__.py`:
```python
```

`server/app/api/v1/__init__.py`:
```python
```

`server/app/api/v1/router.py`:
```python
from fastapi import APIRouter

api_router = APIRouter()
```

- [ ] **Step 7: 创建Docker和docker-compose**

`server/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`server/docker-compose.yml`:
```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - mysql
      - redis
    volumes:
      - .:/app

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: life_sim
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A app.infrastructure.tasks.game_tasks worker --loglevel=info
    env_file:
      - .env
    depends_on:
      - redis
      - mysql

volumes:
  mysql_data:
```

- [ ] **Step 8: 安装依赖并验证启动**

Run: `cd /workspace/server && pip install -r requirements.txt 2>&1 | tail -5`
Expected: Successfully installed ...

Run: `cd /workspace/server && python -c "from app.config import get_settings; s = get_settings(); print(s.app_name)"`
Expected: LifeSimulation

- [ ] **Step 9: Commit**

```bash
git add server/
git commit -m "feat(server): initialize project with FastAPI, config, and Docker"
```

---

### Task 2: 数据库连接与ORM模型

**Files:**
- Create: `server/app/infrastructure/__init__.py`
- Create: `server/app/infrastructure/database/__init__.py`
- Create: `server/app/infrastructure/database/connection.py`
- Create: `server/app/infrastructure/database/models.py`
- Create: `server/alembic.ini`
- Create: `server/migrations/env.py`
- Create: `server/migrations/versions/001_initial.py`
- Test: `server/tests/conftest.py`

- [ ] **Step 1: 创建数据库连接模块**

`server/app/infrastructure/database/connection.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 2: 创建ORM模型**

`server/app/infrastructure/database/models.py`:
```python
from datetime import datetime
from sqlalchemy import (
    Column, BigInteger, String, Integer, Float, Boolean,
    Text, DateTime, JSON, Enum, DECIMAL, ForeignKey, Index,
)
from sqlalchemy.orm import relationship
from app.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
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

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum("male", "female"), nullable=False)
    birth_year = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    stage = Column(String(20), nullable=False, default="infant")
    is_alive = Column(Boolean, nullable=False, default=True)
    city_id = Column(BigInteger, ForeignKey("cities.id"), nullable=False)
    lifespan = Column(Integer, nullable=False, default=75)
    death_cause = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserModel", back_populates="characters")
    stats = relationship("CharacterStatsModel", back_populates="character", uselist=False)
    life_records = relationship("LifeRecordModel", back_populates="character")
    relationships = relationship("RelationshipModel", back_populates="character")
    assets = relationship("AssetModel", back_populates="character")
    city = relationship("CityModel")


class CharacterStatsModel(Base):
    __tablename__ = "character_stats"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, ForeignKey("characters.id"), unique=True, nullable=False)
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

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, ForeignKey("characters.id"), nullable=False)
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

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    stage = Column(String(20), nullable=False)
    category = Column(String(30), nullable=False)
    trigger_condition = Column(JSON, nullable=False)
    probability = Column(Float, nullable=False, default=1.0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    results = relationship("EventResultModel", back_populates="event")

    __table_args__ = (
        Index("idx_events_stage_category", "stage", "category"),
    )


class EventResultModel(Base):
    __tablename__ = "event_results"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey("events.id"), nullable=False, index=True)
    choice_text = Column(String(200), nullable=False)
    choice_index = Column(Integer, nullable=False)
    effects = Column(JSON, nullable=False)
    narrative = Column(Text, nullable=False)
    next_event_id = Column(BigInteger, ForeignKey("events.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    event = relationship("EventModel", back_populates="results", foreign_keys=[event_id])


class RelationshipModel(Base):
    __tablename__ = "relationships"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, ForeignKey("characters.id"), nullable=False, index=True)
    target_name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    intimacy = Column(Integer, nullable=False, default=50)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    character = relationship("CharacterModel", back_populates="relationships")


class CityModel(Base):
    __tablename__ = "cities"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    population = Column(Integer, nullable=False)
    development_index = Column(Float, nullable=False)
    cost_of_living = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
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

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    character_id = Column(BigInteger, ForeignKey("characters.id"), nullable=False)
    type = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(DECIMAL(12, 2), nullable=False)
    acquired_age = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    character = relationship("CharacterModel", back_populates="assets")


class WorldStateModel(Base):
    __tablename__ = "world_states"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    year = Column(Integer, unique=True, nullable=False, index=True)
    era = Column(String(30), nullable=False)
    gdp_index = Column(Float, nullable=False)
    tech_level = Column(Integer, nullable=False)
    major_events = Column(JSON, nullable=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
```

- [ ] **Step 3: 创建Alembic配置**

`server/alembic.ini`:
```ini
[alembic]
script_location = migrations
sqlalchemy.url = mysql+pymysql://root:password@localhost:3306/life_sim

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

`server/migrations/env.py`:
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.infrastructure.database.connection import Base
from app.infrastructure.database.models import *  # noqa: F401,F403
from app.config import get_settings

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 4: 创建初始迁移**

`server/migrations/versions/001_initial.py`:
```python
"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-04
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
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

    op.create_table(
        "jobs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("min_intelligence", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("min_charisma", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("salary_range", sa.JSON(), nullable=False),
        sa.Column("stress_level", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("health_impact", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

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

    op.create_table(
        "characters",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("gender", mysql.ENUM("male", "female"), nullable=False),
        sa.Column("birth_year", sa.Integer(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("stage", sa.String(20), nullable=False, server_default="infant"),
        sa.Column("is_alive", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("city_id", sa.BigInteger(), nullable=False),
        sa.Column("lifespan", sa.Integer(), nullable=False, server_default="75"),
        sa.Column("death_cause", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
    )
    op.create_index("idx_characters_user_id", "characters", ["user_id"])
    op.create_index("idx_characters_stage", "characters", ["stage"])

    op.create_table(
        "character_stats",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("character_id", sa.BigInteger(), nullable=False),
        sa.Column("health", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("intelligence", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("charisma", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("wealth", sa.Integer(), nullable=False, server_default="30"),
        sa.Column("happiness", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("luck", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
        sa.UniqueConstraint("character_id"),
    )

    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("stage", sa.String(20), nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("trigger_condition", sa.JSON(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_events_stage_category", "events", ["stage", "category"])

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
    op.create_index("idx_event_results_event_id", "event_results", ["event_id"])

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

    op.create_table(
        "relationships",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("character_id", sa.BigInteger(), nullable=False),
        sa.Column("target_name", sa.String(50), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("intimacy", sa.Integer(), nullable=False, server_default="50"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["character_id"], ["characters.id"]),
    )
    op.create_index("idx_relationships_character_id", "relationships", ["character_id"])

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


def downgrade():
    op.drop_table("assets")
    op.drop_table("relationships")
    op.drop_table("life_records")
    op.drop_table("event_results")
    op.drop_table("events")
    op.drop_table("character_stats")
    op.drop_table("characters")
    op.drop_table("users")
    op.drop_table("world_states")
    op.drop_table("jobs")
    op.drop_table("cities")
```

- [ ] **Step 5: 创建测试conftest**

`server/tests/__init__.py`:
```python
```

`server/tests/conftest.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.connection import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    import asyncio

    transport = ASGITransport(app=app)

    async def _client():
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c

    return _client()
```

- [ ] **Step 6: 验证模型导入无误**

Run: `cd /workspace/server && python -c "from app.infrastructure.database.models import UserModel, CharacterModel, CharacterStatsModel, EventModel; print('Models imported successfully')"`
Expected: Models imported successfully

- [ ] **Step 7: Commit**

```bash
git add server/
git commit -m "feat(server): add database models, migrations, and test fixtures"
```

---

### Task 3: 领域实体与Repository接口

**Files:**
- Create: `server/app/domain/__init__.py`
- Create: `server/app/domain/entities/__init__.py`
- Create: `server/app/domain/entities/user.py`
- Create: `server/app/domain/entities/character.py`
- Create: `server/app/domain/entities/event.py`
- Create: `server/app/domain/entities/world.py`
- Create: `server/app/domain/interfaces/__init__.py`
- Create: `server/app/domain/interfaces/repository.py`
- Test: `server/tests/unit/__init__.py`

- [ ] **Step 1: 创建用户领域实体**

`server/app/domain/entities/user.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int] = None
    openid: str = ""
    union_id: Optional[str] = None
    phone: Optional[str] = None
    nickname: str = ""
    avatar_url: Optional[str] = None
    platform: str = ""
    last_login_at: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def has_phone(self) -> bool:
        return self.phone is not None and self.phone != ""
```

- [ ] **Step 2: 创建角色领域实体**

`server/app/domain/entities/character.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class LifeStage(str, Enum):
    INFANT = "infant"
    TODDLER = "toddler"
    CHILDHOOD = "childhood"
    ADOLESCENCE = "adolescence"
    YOUTH = "youth"
    PRIME = "prime"
    MIDDLE_AGE = "middle_age"
    ELDERLY = "elderly"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


STAGE_AGE_MAP = {
    LifeStage.INFANT: (0, 3),
    LifeStage.TODDLER: (4, 6),
    LifeStage.CHILDHOOD: (7, 12),
    LifeStage.ADOLESCENCE: (13, 18),
    LifeStage.YOUTH: (19, 30),
    LifeStage.PRIME: (31, 50),
    LifeStage.MIDDLE_AGE: (51, 65),
    LifeStage.ELDERLY: (66, 150),
}


@dataclass
class CharacterStats:
    health: int = 60
    intelligence: int = 50
    charisma: int = 50
    wealth: int = 30
    happiness: int = 60
    luck: int = 50

    def apply_effects(self, effects: dict[str, int]) -> None:
        for attr, delta in effects.items():
            if hasattr(self, attr):
                current = getattr(self, attr)
                setattr(self, attr, max(0, min(100, current + delta)))

    def to_dict(self) -> dict[str, int]:
        return {
            "health": self.health,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "wealth": self.wealth,
            "happiness": self.happiness,
            "luck": self.luck,
        }


@dataclass
class Character:
    id: Optional[int] = None
    user_id: int = 0
    name: str = ""
    gender: Gender = Gender.MALE
    birth_year: int = 2000
    age: int = 0
    stage: LifeStage = LifeStage.INFANT
    is_alive: bool = True
    city_id: int = 1
    lifespan: int = 75
    death_cause: Optional[str] = None
    stats: CharacterStats = field(default_factory=CharacterStats)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def advance_age(self) -> None:
        self.age += 1
        self._update_stage()

    def _update_stage(self) -> None:
        for stage, (min_age, max_age) in STAGE_AGE_MAP.items():
            if min_age <= self.age <= max_age:
                self.stage = stage
                break

    def calculate_effective_lifespan(self) -> int:
        health_modifier = (self.stats.health - 50) * 0.3
        wealth_modifier = (self.stats.wealth - 50) * 0.1
        return int(self.lifespan + health_modifier + wealth_modifier)

    def check_death(self) -> bool:
        if self.stats.health <= 0:
            self.is_alive = False
            self.death_cause = "健康耗尽"
            return True
        effective_lifespan = self.calculate_effective_lifespan()
        if self.age > effective_lifespan:
            import random
            death_probability = (self.age - effective_lifespan) * 0.1
            if random.random() < death_probability:
                self.is_alive = False
                self.death_cause = "自然衰老"
                return True
        return False
```

- [ ] **Step 3: 创建事件领域实体**

`server/app/domain/entities/event.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class EventResult:
    id: Optional[int] = None
    event_id: int = 0
    choice_text: str = ""
    choice_index: int = 0
    effects: dict = field(default_factory=dict)
    narrative: str = ""
    next_event_id: Optional[int] = None


@dataclass
class Event:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    stage: str = ""
    category: str = ""
    trigger_condition: dict = field(default_factory=dict)
    probability: float = 1.0
    is_active: bool = True
    results: list[EventResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class PendingEvent:
    """角色当前待处理的事件（含选项）"""
    event: Event = field(default_factory=Event)
    character_id: int = 0
```

- [ ] **Step 4: 创建世界领域实体**

`server/app/domain/entities/world.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class City:
    id: Optional[int] = None
    name: str = ""
    region: str = ""
    population: int = 0
    development_index: float = 0.5
    cost_of_living: float = 0.5


@dataclass
class Job:
    id: Optional[int] = None
    name: str = ""
    category: str = ""
    min_intelligence: int = 0
    min_charisma: int = 0
    salary_range: dict = field(default_factory=lambda: {"min": 3000, "max": 8000})
    stress_level: int = 50
    health_impact: int = 0


@dataclass
class WorldState:
    id: Optional[int] = None
    year: int = 2000
    era: str = ""
    gdp_index: float = 0.5
    tech_level: int = 5
    major_events: list = field(default_factory=list)
    updated_at: datetime = field(default_factory=datetime.utcnow)
```

- [ ] **Step 5: 创建Repository抽象接口**

`server/app/domain/interfaces/repository.py`:
```python
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User
from app.domain.entities.character import Character, CharacterStats
from app.domain.entities.event import Event, EventResult
from app.domain.entities.world import City, Job, WorldState


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    async def get_by_openid(self, openid: str) -> Optional[User]: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...


class ICharacterRepository(ABC):
    @abstractmethod
    async def get_by_id(self, character_id: int) -> Optional[Character]: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[Character]: ...

    @abstractmethod
    async def create(self, character: Character) -> Character: ...

    @abstractmethod
    async def update(self, character: Character) -> Character: ...

    @abstractmethod
    async def get_stats(self, character_id: int) -> Optional[CharacterStats]: ...

    @abstractmethod
    async def update_stats(self, character_id: int, stats: CharacterStats) -> CharacterStats: ...


class IEventRepository(ABC):
    @abstractmethod
    async def get_by_id(self, event_id: int) -> Optional[Event]: ...

    @abstractmethod
    async def get_by_stage(self, stage: str) -> list[Event]: ...

    @abstractmethod
    async def get_results(self, event_id: int) -> list[EventResult]: ...

    @abstractmethod
    async def get_result_by_choice(self, event_id: int, choice_index: int) -> Optional[EventResult]: ...


class IWorldRepository(ABC):
    @abstractmethod
    async def get_cities(self) -> list[City]: ...

    @abstractmethod
    async def get_city_by_id(self, city_id: int) -> Optional[City]: ...

    @abstractmethod
    async def get_jobs(self) -> list[Job]: ...

    @abstractmethod
    async def get_world_state(self, year: int) -> Optional[WorldState]: ...
```

- [ ] **Step 6: 编写领域实体单元测试**

`server/tests/unit/__init__.py`:
```python
```

`server/tests/unit/test_character_entity.py`:
```python
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
        stats = CharacterStats(health=60, intelligence=50, charisma=50, wealth=30, happiness=60, luck=50)
        d = stats.to_dict()
        assert d == {"health": 60, "intelligence": 50, "charisma": 50, "wealth": 30, "happiness": 60, "luck": 50}


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
```

- [ ] **Step 7: 运行测试**

Run: `cd /workspace/server && python -m pytest tests/unit/test_character_entity.py -v`
Expected: 7 passed

- [ ] **Step 8: Commit**

```bash
git add server/
git commit -m "feat(server): add domain entities, repository interfaces, and character unit tests"
```

---

### Task 4: Repository实现

**Files:**
- Create: `server/app/infrastructure/repositories/__init__.py`
- Create: `server/app/infrastructure/repositories/user_repo.py`
- Create: `server/app/infrastructure/repositories/character_repo.py`
- Create: `server/app/infrastructure/repositories/event_repo.py`
- Create: `server/app/infrastructure/cache/__init__.py`
- Create: `server/app/infrastructure/cache/redis_client.py`

- [ ] **Step 1: 创建Redis客户端**

`server/app/infrastructure/cache/__init__.py`:
```python
```

`server/app/infrastructure/cache/redis_client.py`:
```python
import redis.asyncio as redis
from app.config import get_settings

settings = get_settings()

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


async def get_redis() -> redis.Redis:
    return redis_client
```

- [ ] **Step 2: 创建UserRepository**

`server/app/infrastructure/repositories/user_repo.py`:
```python
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.interfaces.repository import IUserRepository
from app.infrastructure.database.models import UserModel


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    async def get_by_openid(self, openid: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.openid == openid).first()
        return self._to_entity(model) if model else None

    async def create(self, user: User) -> User:
        model = UserModel(
            openid=user.openid,
            union_id=user.union_id,
            phone=user.phone,
            nickname=user.nickname,
            avatar_url=user.avatar_url,
            platform=user.platform,
            last_login_at=user.last_login_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not model:
            raise ValueError(f"User {user.id} not found")
        model.nickname = user.nickname
        model.avatar_url = user.avatar_url
        model.phone = user.phone
        model.union_id = user.union_id
        model.last_login_at = user.last_login_at
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            openid=model.openid,
            union_id=model.union_id,
            phone=model.phone,
            nickname=model.nickname,
            avatar_url=model.avatar_url,
            platform=model.platform,
            last_login_at=model.last_login_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
```

- [ ] **Step 3: 创建CharacterRepository**

`server/app/infrastructure/repositories/character_repo.py`:
```python
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
```

- [ ] **Step 4: 创建EventRepository**

`server/app/infrastructure/repositories/event_repo.py`:
```python
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.event import Event, EventResult
from app.domain.interfaces.repository import IEventRepository
from app.infrastructure.database.models import EventModel, EventResultModel


class EventRepository(IEventRepository):
    def __init__(self, db: Session):
        self.db = db

    async def get_by_id(self, event_id: int) -> Optional[Event]:
        model = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        if not model:
            return None
        return self._to_entity(model)

    async def get_by_stage(self, stage: str) -> list[Event]:
        models = (
            self.db.query(EventModel)
            .filter(EventModel.stage == stage, EventModel.is_active == True)
            .all()
        )
        return [self._to_entity(m) for m in models]

    async def get_results(self, event_id: int) -> list[EventResult]:
        models = (
            self.db.query(EventResultModel)
            .filter(EventResultModel.event_id == event_id)
            .order_by(EventResultModel.choice_index)
            .all()
        )
        return [self._result_to_entity(m) for m in models]

    async def get_result_by_choice(self, event_id: int, choice_index: int) -> Optional[EventResult]:
        model = (
            self.db.query(EventResultModel)
            .filter(EventResultModel.event_id == event_id, EventResultModel.choice_index == choice_index)
            .first()
        )
        return self._result_to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: EventModel) -> Event:
        results = [EventRepository._result_to_entity(r) for r in model.results]
        return Event(
            id=model.id,
            title=model.title,
            description=model.description,
            stage=model.stage,
            category=model.category,
            trigger_condition=model.trigger_condition,
            probability=model.probability,
            is_active=model.is_active,
            results=results,
            created_at=model.created_at,
        )

    @staticmethod
    def _result_to_entity(model: EventResultModel) -> EventResult:
        return EventResult(
            id=model.id,
            event_id=model.event_id,
            choice_text=model.choice_text,
            choice_index=model.choice_index,
            effects=model.effects,
            narrative=model.narrative,
            next_event_id=model.next_event_id,
        )
```

- [ ] **Step 5: 验证导入**

Run: `cd /workspace/server && python -c "from app.infrastructure.repositories.user_repo import UserRepository; from app.infrastructure.repositories.character_repo import CharacterRepository; from app.infrastructure.repositories.event_repo import EventRepository; print('Repositories imported successfully')"`
Expected: Repositories imported successfully

- [ ] **Step 6: Commit**

```bash
git add server/
git commit -m "feat(server): add repository implementations for user, character, and event"
```

---

### Task 5: 规则引擎与领域服务

**Files:**
- Create: `server/app/domain/services/__init__.py`
- Create: `server/app/domain/services/rule_engine.py`
- Create: `server/app/domain/services/time_service.py`
- Create: `server/app/domain/services/event_service.py`
- Create: `server/app/domain/services/game_engine.py`
- Test: `server/tests/unit/test_rule_engine.py`
- Test: `server/tests/unit/test_time_service.py`
- Test: `server/tests/unit/test_game_engine.py`

- [ ] **Step 1: 创建规则引擎**

`server/app/domain/services/__init__.py`:
```python
```

`server/app/domain/services/rule_engine.py`:
```python
import random
import logging
from app.domain.entities.character import Character, LifeStage
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

    def calculate_natural_stat_changes(self, character: Character) -> dict[str, int]:
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

        # 财富变化（受职业影响，MVP简化）
        if 25 <= age <= 55:
            changes["wealth"] = random.randint(0, 3)
        else:
            changes["wealth"] = random.randint(-2, 1)

        # 幸福变化
        changes["happiness"] = random.randint(-3, 3)

        # 运气变化
        changes["luck"] = random.randint(-5, 5)

        return changes
```

- [ ] **Step 2: 编写规则引擎测试**

`server/tests/unit/test_rule_engine.py`:
```python
import pytest
from app.domain.services.rule_engine import RuleEngine
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender
from app.domain.entities.event import Event, EventResult


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
                id=1,
                title="入学",
                stage="childhood",
                category="milestone",
                trigger_condition={"min_age": 7, "max_age": 7},
                probability=1.0,
            ),
        ]
        result = self.engine.evaluate_events(self.character, events)
        assert len(result) == 1
        assert result[0].title == "入学"

    def test_evaluate_events_condition_fail_age(self):
        events = [
            Event(
                id=1,
                title="高考",
                stage="adolescence",
                category="milestone",
                trigger_condition={"min_age": 18, "max_age": 18},
                probability=1.0,
            ),
        ]
        result = self.engine.evaluate_events(self.character, events)
        assert len(result) == 0

    def test_evaluate_events_condition_fail_stat(self):
        events = [
            Event(
                id=1,
                title="天才班",
                stage="childhood",
                category="milestone",
                trigger_condition={"stats": {"intelligence": 90}},
                probability=1.0,
            ),
        ]
        result = self.engine.evaluate_events(self.character, events)
        assert len(result) == 0

    def test_evaluate_events_max_limit(self):
        events = [
            Event(id=i, title=f"Event {i}", stage="childhood", category="random", trigger_condition={}, probability=1.0)
            for i in range(10)
        ]
        result = self.engine.evaluate_events(self.character, events, max_events=3)
        assert len(result) <= 3

    def test_calculate_natural_stat_changes_young(self):
        char = Character(age=10, stats=CharacterStats())
        changes = self.engine.calculate_natural_stat_changes(char)
        assert "health" in changes
        assert "intelligence" in changes
        assert changes["intelligence"] >= 1  # 年轻时智力增长

    def test_calculate_natural_stat_changes_old(self):
        char = Character(age=70, stats=CharacterStats())
        changes = self.engine.calculate_natural_stat_changes(char)
        assert changes["health"] <= -1  # 老年健康下降
```

- [ ] **Step 3: 运行规则引擎测试**

Run: `cd /workspace/server && python -m pytest tests/unit/test_rule_engine.py -v`
Expected: 6 passed

- [ ] **Step 4: 创建时间服务**

`server/app/domain/services/time_service.py`:
```python
import logging
from app.domain.entities.character import Character, LifeStage
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
```

- [ ] **Step 5: 创建事件服务**

`server/app/domain/services/event_service.py`:
```python
import logging
from app.domain.entities.character import Character
from app.domain.entities.event import Event, EventResult
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
```

- [ ] **Step 6: 创建游戏引擎**

`server/app/domain/services/game_engine.py`:
```python
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
```

- [ ] **Step 7: 编写游戏引擎集成测试**

`server/tests/unit/test_game_engine.py`:
```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.services.game_engine import GameEngine
from app.domain.services.rule_engine import RuleEngine
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender
from app.domain.entities.event import Event, EventResult


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
```

- [ ] **Step 8: 运行所有单元测试**

Run: `cd /workspace/server && python -m pytest tests/unit/ -v`
Expected: all passed

- [ ] **Step 9: Commit**

```bash
git add server/
git commit -m "feat(server): add rule engine, time service, event service, and game engine"
```

---

### Task 6: Pydantic Schemas

**Files:**
- Create: `server/app/schemas/__init__.py`
- Create: `server/app/schemas/auth.py`
- Create: `server/app/schemas/character.py`
- Create: `server/app/schemas/event.py`
- Create: `server/app/schemas/world.py`

- [ ] **Step 1: 创建认证Schemas**

`server/app/schemas/auth.py`:
```python
from pydantic import BaseModel, Field
from typing import Optional


class WechatLoginRequest(BaseModel):
    code: str = Field(..., min_length=1, description="微信登录code")
    platform: str = Field(default="wechat", pattern="^(wechat|ios|android)$")


class PhoneBindRequest(BaseModel):
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")
    verify_code: str = Field(..., min_length=4, max_length=6, description="验证码")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserBrief"


class UserBrief(BaseModel):
    id: int
    nickname: str
    avatar_url: Optional[str] = None
    has_phone: bool


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserProfileResponse(BaseModel):
    id: int
    nickname: str
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    platform: str
    has_phone: bool
```

- [ ] **Step 2: 创建角色Schemas**

`server/app/schemas/character.py`:
```python
from pydantic import BaseModel, Field
from typing import Optional


class CreateCharacterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="角色姓名")
    gender: str = Field(..., pattern="^(male|female)$", description="性别")
    city_id: int = Field(..., gt=0, description="出生城市ID")


class CharacterStatsResponse(BaseModel):
    health: int
    intelligence: int
    charisma: int
    wealth: int
    happiness: int
    luck: int


class CityBrief(BaseModel):
    id: int
    name: str


class CharacterResponse(BaseModel):
    id: int
    name: str
    gender: str
    age: int
    stage: str
    is_alive: bool
    city: Optional[CityBrief] = None
    stats: Optional[CharacterStatsResponse] = None


class CharacterListResponse(BaseModel):
    characters: list[CharacterResponse]
    total: int


class LifeRecordResponse(BaseModel):
    id: int
    age: int
    year: int
    summary: str
    stat_changes: Optional[dict] = None


class AdvanceYearResponse(BaseModel):
    character: dict
    year_summary: dict
    pending_events: list[dict]
```

- [ ] **Step 3: 创建事件Schemas**

`server/app/schemas/event.py`:
```python
from pydantic import BaseModel, Field


class EventChoiceRequest(BaseModel):
    character_id: int = Field(..., gt=0)
    choice_index: int = Field(..., ge=0)


class EventChoiceBrief(BaseModel):
    index: int
    text: str


class PendingEventResponse(BaseModel):
    id: int
    title: str
    description: str
    choices: list[EventChoiceBrief]


class EventChoiceResultResponse(BaseModel):
    narrative: str
    effects: dict
    new_stats: dict
    triggered_events: list[dict]
```

- [ ] **Step 4: 创建世界Schemas**

`server/app/schemas/world.py`:
```python
from pydantic import BaseModel
from typing import Optional


class CityResponse(BaseModel):
    id: int
    name: str
    region: str
    population: int
    development_index: float
    cost_of_living: float


class JobResponse(BaseModel):
    id: int
    name: str
    category: str
    min_intelligence: int
    min_charisma: int
    salary_range: dict
    stress_level: int
    health_impact: int


class WorldStateResponse(BaseModel):
    year: int
    era: str
    gdp_index: float
    tech_level: int
    major_events: Optional[list] = None
```

- [ ] **Step 5: 验证Schema导入**

Run: `cd /workspace/server && python -c "from app.schemas.auth import WechatLoginRequest, TokenResponse; from app.schemas.character import CreateCharacterRequest; from app.schemas.event import EventChoiceRequest; print('Schemas imported successfully')"`
Expected: Schemas imported successfully

- [ ] **Step 6: Commit**

```bash
git add server/
git commit -m "feat(server): add Pydantic schemas for all API request/response models"
```

---

### Task 7: API端点实现

**Files:**
- Create: `server/app/api/deps.py`
- Modify: `server/app/api/v1/router.py`
- Create: `server/app/api/v1/auth.py`
- Create: `server/app/api/v1/characters.py`
- Create: `server/app/api/v1/events.py`
- Create: `server/app/api/v1/world.py`

- [ ] **Step 1: 创建依赖注入模块**

`server/app/api/deps.py`:
```python
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.user_repo import UserRepository
from app.infrastructure.repositories.character_repo import CharacterRepository
from app.infrastructure.repositories.event_repo import EventRepository
from app.domain.interfaces.repository import IUserRepository, ICharacterRepository, IEventRepository
from app.domain.entities.user import User

settings = get_settings()
security = HTTPBearer()


def get_user_repo(db: Session = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)


def get_character_repo(db: Session = Depends(get_db)) -> ICharacterRepository:
    return CharacterRepository(db)


def get_event_repo(db: Session = Depends(get_db)) -> IEventRepository:
    return EventRepository(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo: IUserRepository = Depends(get_user_repo),
) -> User:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
```

- [ ] **Step 2: 创建认证API**

`server/app/api/v1/auth.py`:
```python
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt

from app.config import get_settings
from app.api.deps import get_user_repo, get_current_user
from app.domain.interfaces.repository import IUserRepository
from app.domain.entities.user import User
from app.schemas.auth import (
    WechatLoginRequest,
    PhoneBindRequest,
    TokenResponse,
    UserBrief,
    RefreshTokenRequest,
    UserProfileResponse,
)

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    return jwt.encode({"sub": user_id, "exp": expire}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
    return jwt.encode({"sub": user_id, "exp": expire, "type": "refresh"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


@router.post("/wechat-login", response_model=TokenResponse)
async def wechat_login(
    request: WechatLoginRequest,
    user_repo: IUserRepository = Depends(get_user_repo),
):
    """微信登录：用code换取openid，创建或获取用户"""
    # MVP阶段：简化微信登录流程，直接用code作为openid
    # 生产环境需要调用微信API: https://api.weixin.qq.com/sns/jscode2session
    openid = f"wx_{request.code}"

    user = await user_repo.get_by_openid(openid)
    if not user:
        user = User(
            openid=openid,
            nickname=f"玩家{openid[-4:]}",
            platform=request.platform,
            last_login_at=datetime.utcnow(),
        )
        user = await user_repo.create(user)
    else:
        user.last_login_at = datetime.utcnow()
        user = await user_repo.update(user)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
        user=UserBrief(
            id=user.id,
            nickname=user.nickname,
            avatar_url=user.avatar_url,
            has_phone=user.has_phone,
        ),
    )


@router.post("/phone-bind")
async def bind_phone(
    request: PhoneBindRequest,
    current_user: User = Depends(get_current_user),
    user_repo: IUserRepository = Depends(get_user_repo),
):
    """绑定手机号"""
    current_user.phone = request.phone
    user = await user_repo.update(current_user)
    return {"message": "Phone bound successfully", "phone": user.phone}


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest):
    """刷新Token"""
    try:
        payload = jwt.decode(request.refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user_id = payload.get("sub")
        access_token = create_access_token(user_id)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserProfileResponse(
        id=current_user.id,
        nickname=current_user.nickname,
        avatar_url=current_user.avatar_url,
        phone=current_user.phone,
        platform=current_user.platform,
        has_phone=current_user.has_phone,
    )
```

- [ ] **Step 3: 创建角色API**

`server/app/api/v1/characters.py`:
```python
import random
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_character_repo, get_current_user, get_event_repo
from app.domain.interfaces.repository import ICharacterRepository, IEventRepository
from app.domain.entities.user import User
from app.domain.entities.character import Character, CharacterStats, LifeStage, Gender
from app.domain.services.rule_engine import RuleEngine
from app.domain.services.game_engine import GameEngine
from app.schemas.character import (
    CreateCharacterRequest,
    CharacterResponse,
    CharacterStatsResponse,
    CityBrief,
    AdvanceYearResponse,
)

router = APIRouter(prefix="/characters", tags=["characters"])


@router.post("", response_model=CharacterResponse)
async def create_character(
    request: CreateCharacterRequest,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
):
    """创建新角色"""
    stats = CharacterStats(
        health=random.randint(50, 80),
        intelligence=random.randint(30, 70),
        charisma=random.randint(30, 70),
        wealth=random.randint(20, 50),
        happiness=random.randint(50, 80),
        luck=random.randint(30, 70),
    )
    character = Character(
        user_id=current_user.id,
        name=request.name,
        gender=Gender(request.gender),
        city_id=request.city_id,
        stats=stats,
    )
    character = await char_repo.create(character)

    return CharacterResponse(
        id=character.id,
        name=character.name,
        gender=character.gender.value,
        age=character.age,
        stage=character.stage.value,
        is_alive=character.is_alive,
        stats=CharacterStatsResponse(**character.stats.to_dict()),
    )


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: int,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
):
    """获取角色详情"""
    character = await char_repo.get_by_id(character_id)
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    stats = await char_repo.get_stats(character_id)
    return CharacterResponse(
        id=character.id,
        name=character.name,
        gender=character.gender.value,
        age=character.age,
        stage=character.stage.value,
        is_alive=character.is_alive,
        stats=CharacterStatsResponse(**stats.to_dict()) if stats else None,
    )


@router.get("/{character_id}/stats", response_model=CharacterStatsResponse)
async def get_character_stats(
    character_id: int,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
):
    """获取角色属性"""
    character = await char_repo.get_by_id(character_id)
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    stats = await char_repo.get_stats(character_id)
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stats not found")
    return CharacterStatsResponse(**stats.to_dict())


@router.post("/{character_id}/advance", response_model=AdvanceYearResponse)
async def advance_year(
    character_id: int,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
    event_repo: IEventRepository = Depends(get_event_repo),
):
    """推进时间1年"""
    character = await char_repo.get_by_id(character_id)
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    rule_engine = RuleEngine()
    game_engine = GameEngine(char_repo, event_repo, rule_engine)

    try:
        result = await game_engine.advance_character(character_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return AdvanceYearResponse(**result)
```

- [ ] **Step 4: 创建事件API**

`server/app/api/v1/events.py`:
```python
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_character_repo, get_current_user, get_event_repo
from app.domain.interfaces.repository import ICharacterRepository, IEventRepository
from app.domain.entities.user import User
from app.domain.services.rule_engine import RuleEngine
from app.domain.services.event_service import EventService
from app.schemas.event import EventChoiceRequest, EventChoiceResultResponse, PendingEventResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/pending/{character_id}", response_model=list[PendingEventResponse])
async def get_pending_events(
    character_id: int,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
    event_repo: IEventRepository = Depends(get_event_repo),
):
    """获取角色待处理事件"""
    character = await char_repo.get_by_id(character_id)
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    rule_engine = RuleEngine()
    event_service = EventService(event_repo, rule_engine)
    events = await event_service.get_pending_events(character)

    return [
        PendingEventResponse(
            id=e.id,
            title=e.title,
            description=e.description,
            choices=[{"index": r.choice_index, "text": r.choice_text} for r in e.results],
        )
        for e in events
    ]


@router.post("/{event_id}/choose", response_model=EventChoiceResultResponse)
async def choose_event_option(
    event_id: int,
    request: EventChoiceRequest,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
    event_repo: IEventRepository = Depends(get_event_repo),
):
    """选择事件选项"""
    character = await char_repo.get_by_id(request.character_id)
    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    rule_engine = RuleEngine()
    event_service = EventService(event_repo, rule_engine)

    try:
        result = await event_service.choose_event_option(event_id, request.choice_index, character)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    await char_repo.update_stats(character.id, character.stats)

    return EventChoiceResultResponse(**result)
```

- [ ] **Step 5: 创建世界API**

`server/app/api/v1/world.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.models import CityModel, JobModel, WorldStateModel
from app.schemas.world import CityResponse, JobResponse, WorldStateResponse

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/state", response_model=WorldStateResponse)
async def get_world_state(db: Session = Depends(get_db)):
    """获取当前世界状态"""
    state = db.query(WorldStateModel).order_by(WorldStateModel.year.desc()).first()
    if not state:
        return WorldStateResponse(year=2000, era="信息时代", gdp_index=0.5, tech_level=5)
    return WorldStateResponse(
        year=state.year,
        era=state.era,
        gdp_index=state.gdp_index,
        tech_level=state.tech_level,
        major_events=state.major_events,
    )


@router.get("/cities", response_model=list[CityResponse])
async def get_cities(db: Session = Depends(get_db)):
    """获取城市列表"""
    cities = db.query(CityModel).all()
    return [
        CityResponse(
            id=c.id, name=c.name, region=c.region,
            population=c.population, development_index=c.development_index,
            cost_of_living=c.cost_of_living,
        )
        for c in cities
    ]


@router.get("/jobs", response_model=list[JobResponse])
async def get_jobs(db: Session = Depends(get_db)):
    """获取职业列表"""
    jobs = db.query(JobModel).all()
    return [
        JobResponse(
            id=j.id, name=j.name, category=j.category,
            min_intelligence=j.min_intelligence, min_charisma=j.min_charisma,
            salary_range=j.salary_range, stress_level=j.stress_level,
            health_impact=j.health_impact,
        )
        for j in jobs
    ]
```

- [ ] **Step 6: 更新路由聚合**

`server/app/api/v1/router.py`:
```python
from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.characters import router as characters_router
from app.api.v1.events import router as events_router
from app.api.v1.world import router as world_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(characters_router)
api_router.include_router(events_router)
api_router.include_router(world_router)
```

- [ ] **Step 7: 验证API启动**

Run: `cd /workspace/server && python -c "from app.main import app; routes = [r.path for r in app.routes]; print(f'Routes: {len(routes)}')"`
Expected: Routes count > 10

- [ ] **Step 8: Commit**

```bash
git add server/
git commit -m "feat(server): add all API endpoints - auth, characters, events, world"
```

---

### Task 8: 种子数据

**Files:**
- Create: `server/app/infrastructure/database/seed.py`

- [ ] **Step 1: 创建种子数据脚本**

`server/app/infrastructure/database/seed.py`:
```python
"""种子数据：初始城市、职业、事件数据"""
from sqlalchemy.orm import Session
from app.infrastructure.database.models import CityModel, JobModel, EventModel, EventResultModel, WorldStateModel


def seed_cities(db: Session) -> None:
    cities = [
        CityModel(name="北京", region="华北", population=21540000, development_index=0.95, cost_of_living=0.9),
        CityModel(name="上海", region="华东", population=24870000, development_index=0.95, cost_of_living=0.92),
        CityModel(name="广州", region="华南", population=18680000, development_index=0.88, cost_of_living=0.75),
        CityModel(name="深圳", region="华南", population=17560000, development_index=0.92, cost_of_living=0.85),
        CityModel(name="成都", region="西南", population=20940000, development_index=0.78, cost_of_living=0.6),
        CityModel(name="杭州", region="华东", population=11940000, development_index=0.85, cost_of_living=0.72),
        CityModel(name="武汉", region="华中", population=12327000, development_index=0.75, cost_of_living=0.58),
        CityModel(name="西安", region="西北", population=12953000, development_index=0.7, cost_of_living=0.55),
        CityModel(name="南京", region="华东", population=9314000, development_index=0.82, cost_of_living=0.68),
        CityModel(name="重庆", region="西南", population=32054000, development_index=0.72, cost_of_living=0.52),
    ]
    db.add_all(cities)
    db.commit()


def seed_jobs(db: Session) -> None:
    jobs = [
        JobModel(name="程序员", category="科技", min_intelligence=60, min_charisma=30, salary_range={"min": 8000, "max": 35000}, stress_level=70, health_impact=-5),
        JobModel(name="教师", category="教育", min_intelligence=55, min_charisma=50, salary_range={"min": 5000, "max": 12000}, stress_level=55, health_impact=-2),
        JobModel(name="医生", category="医疗", min_intelligence=70, min_charisma=40, salary_range={"min": 8000, "max": 30000}, stress_level=80, health_impact=-8),
        JobModel(name="公务员", category="政府", min_intelligence=50, min_charisma=45, salary_range={"min": 6000, "max": 15000}, stress_level=40, health_impact=0),
        JobModel(name="销售", category="商业", min_intelligence=35, min_charisma=65, salary_range={"min": 4000, "max": 20000}, stress_level=65, health_impact=-3),
        JobModel(name="工人", category="制造", min_intelligence=25, min_charisma=20, salary_range={"min": 4000, "max": 8000}, stress_level=50, health_impact=-10),
        JobModel(name="艺术家", category="文化", min_intelligence=45, min_charisma=60, salary_range={"min": 3000, "max": 50000}, stress_level=60, health_impact=-2),
        JobModel(name="厨师", category="餐饮", min_intelligence=30, min_charisma=35, salary_range={"min": 4000, "max": 15000}, stress_level=60, health_impact=-5),
        JobModel(name="律师", category="法律", min_intelligence=65, min_charisma=55, salary_range={"min": 8000, "max": 40000}, stress_level=75, health_impact=-5),
        JobModel(name="创业者", category="商业", min_intelligence=55, min_charisma=60, salary_range={"min": 0, "max": 100000}, stress_level=90, health_impact=-10),
    ]
    db.add_all(jobs)
    db.commit()


def seed_events(db: Session) -> None:
    """种子事件数据（MVP首批）"""
    events_data = [
        # 少年期事件
        {
            "event": EventModel(title="入学第一天", description="你背着新书包走进了小学的校门，一切都是那么新鲜。", stage="childhood", category="milestone", trigger_condition={"min_age": 7, "max_age": 7}, probability=1.0),
            "results": [
                EventResultModel(choice_text="认真听讲，做个好学生", choice_index=0, effects={"intelligence": 5, "happiness": -2}, narrative="你认真听讲，老师很快就注意到了你，让你当了小组长。"),
                EventResultModel(choice_text="和同学们打成一片", choice_index=1, effects={"charisma": 5, "happiness": 3}, narrative="你很快就交到了一群好朋友，课间总是最热闹的那个。"),
                EventResultModel(choice_text="对一切都感到害怕", choice_index=2, effects={"happiness": -5, "intelligence": 2}, narrative="你躲在角落里不敢说话，但默默观察着一切。"),
            ]
        },
        # 青春期事件
        {
            "event": EventModel(title="中考来了", description="初中三年转瞬即逝，中考的成绩将决定你能否进入重点高中。", stage="adolescence", category="milestone", trigger_condition={"min_age": 15, "max_age": 15, "stats": {"intelligence": 40}}, probability=1.0),
            "results": [
                EventResultModel(choice_text="全力以赴冲刺", choice_index=0, effects={"intelligence": 8, "health": -3, "happiness": -5}, narrative="你拼尽全力复习，虽然过程辛苦，但最终考上了重点高中！"),
                EventResultModel(choice_text="正常发挥就好", choice_index=1, effects={"intelligence": 3, "happiness": 2}, narrative="你保持平常心，发挥稳定，进入了一所普通高中。"),
                EventResultModel(choice_text="不想考了", choice_index=2, effects={"intelligence": -3, "wealth": -5, "happiness": -8}, narrative="你放弃了努力，成绩不理想，只能去一所职业学校。"),
            ]
        },
        {
            "event": EventModel(title="初恋", description="你注意到班上有一个同学，每次看到对方你的心都会怦怦跳。", stage="adolescence", category="social", trigger_condition={"min_age": 14, "max_age": 18, "stats": {"charisma": 35}}, probability=0.6),
            "results": [
                EventResultModel(choice_text="鼓起勇气表白", choice_index=0, effects={"charisma": 5, "happiness": 8, "luck": -2}, narrative="你鼓起勇气表白了，对方红着脸点了点头，你的世界突然变得五彩斑斓。"),
                EventResultModel(choice_text="默默暗恋就好", choice_index=1, effects={"happiness": -3, "intelligence": 2}, narrative="你把这份感情藏在心底，化作了学习的动力。"),
                EventResultModel(choice_text="专注学习，不想这些", choice_index=2, effects={"intelligence": 5, "charisma": -3}, narrative="你强迫自己不去想这些，把精力都放在了书本上。"),
            ]
        },
        # 青年期事件
        {
            "event": EventModel(title="高考", description="十二年寒窗苦读，高考就在眼前。这是改变命运的时刻。", stage="youth", category="milestone", trigger_condition={"min_age": 18, "max_age": 18}, probability=1.0),
            "results": [
                EventResultModel(choice_text="超常发挥", choice_index=0, effects={"intelligence": 10, "happiness": 10, "luck": 5}, narrative="你超常发挥，考出了远超预期的成绩，名校向你敞开了大门！"),
                EventResultModel(choice_text="正常发挥", choice_index=1, effects={"intelligence": 3, "happiness": 2}, narrative="你发挥正常，考上了一所不错的大学。"),
                EventResultModel(choice_text="发挥失常", choice_index=2, effects={"intelligence": -5, "happiness": -10, "luck": -5}, narrative="紧张让你发挥失常，成绩远不如平时，只能选择复读或去一所普通学校。"),
            ]
        },
        {
            "event": EventModel(title="求职面试", description="毕业了，你拿到了一家公司的面试通知。", stage="youth", category="career", trigger_condition={"min_age": 22, "max_age": 25}, probability=0.8),
            "results": [
                EventResultModel(choice_text="精心准备，自信应对", choice_index=0, effects={"wealth": 5, "intelligence": 2, "happiness": 3}, narrative="你准备充分，面试表现出色，顺利拿到了offer！"),
                EventResultModel(choice_text="紧张但努力表现", choice_index=1, effects={"wealth": 2, "happiness": -1}, narrative="虽然有些紧张，但你还是通过了面试，拿到了一份普通的工作。"),
                EventResultModel(choice_text="觉得不合适，放弃面试", choice_index=2, effects={"wealth": -5, "happiness": -3}, narrative="你放弃了这次机会，继续寻找更合适的方向。"),
            ]
        },
        # 壮年期事件
        {
            "event": EventModel(title="体检异常", description="年度体检报告出来了，有几项指标亮了红灯。", stage="prime", category="health", trigger_condition={"min_age": 35, "max_age": 55, "stats": {"health": 50}}, probability=0.5),
            "results": [
                EventResultModel(choice_text="立即就医，调整生活方式", choice_index=0, effects={"health": 5, "wealth": -5, "happiness": -2}, narrative="你开始规律作息、健康饮食，身体逐渐好转。"),
                EventResultModel(choice_text="太忙了，以后再说", choice_index=1, effects={"health": -10, "wealth": 2}, narrative="你继续忙碌的工作，身体状况越来越差。"),
            ]
        },
        {
            "event": EventModel(title="创业机会", description="一个朋友邀请你一起创业，这是一个风险与机遇并存的选择。", stage="prime", category="career", trigger_condition={"min_age": 28, "max_age": 45, "stats": {"intelligence": 50, "charisma": 45}}, probability=0.3),
            "results": [
                EventResultModel(choice_text="全力以赴，辞职创业", choice_index=0, effects={"wealth": -10, "happiness": 5, "health": -5, "luck": 10}, narrative="你辞去了稳定的工作，全身心投入创业。前路未知，但你充满激情。"),
                EventResultModel(choice_text="兼职尝试，稳中求进", choice_index=1, effects={"wealth": -3, "health": -3, "intelligence": 3}, narrative="你在工作之余尝试创业，虽然进展缓慢，但风险可控。"),
                EventResultModel(choice_text="婉拒邀请，保持稳定", choice_index=2, effects={"happiness": -3, "wealth": 2}, narrative="你选择了稳定的生活，但心里总觉得少了些什么。"),
            ]
        },
        # 老年期事件
        {
            "event": EventModel(title="退休生活", description="到了退休的年纪，你终于可以放下工作了。", stage="elderly", category="milestone", trigger_condition={"min_age": 60, "max_age": 65}, probability=1.0),
            "results": [
                EventResultModel(choice_text="环游世界，享受人生", choice_index=0, effects={"happiness": 10, "wealth": -8, "health": -2}, narrative="你开始了环球旅行，看遍了大好河山，人生无憾。"),
                EventResultModel(choice_text="含饴弄孙，安享天伦", choice_index=1, effects={"happiness": 8, "health": 2}, narrative="你在家陪伴孙辈成长，享受着天伦之乐。"),
                EventResultModel(choice_text="发挥余热，继续工作", choice_index=2, effects={"wealth": 5, "health": -5, "happiness": -3}, narrative="你闲不住，继续做一些力所能及的工作。"),
            ]
        },
    ]

    for item in events_data:
        event = item["event"]
        db.add(event)
        db.flush()
        for result in item["results"]:
            result.event_id = event.id
            db.add(result)
    db.commit()


def seed_world_states(db: Session) -> None:
    state = WorldStateModel(year=2000, era="信息时代", gdp_index=0.5, tech_level=5, major_events=["互联网普及"])
    db.add(state)
    db.commit()


def run_all_seeds(db: Session) -> None:
    """执行所有种子数据"""
    seed_cities(db)
    seed_jobs(db)
    seed_events(db)
    seed_world_states(db)
    print("Seed data inserted successfully")
```

- [ ] **Step 2: Commit**

```bash
git add server/
git commit -m "feat(server): add seed data for cities, jobs, events, and world states"
```

---

### Task 9: 集成测试

**Files:**
- Create: `server/tests/integration/__init__.py`
- Create: `server/tests/integration/test_auth_api.py`
- Create: `server/tests/integration/test_character_api.py`

- [ ] **Step 1: 创建认证API集成测试**

`server/tests/integration/test_auth_api.py`:
```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_wechat_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_code_123", "platform": "wechat"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data


@pytest.mark.asyncio
async def test_get_profile():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login_resp = await client.post(
            "/api/v1/auth/wechat-login",
            json={"code": "test_profile", "platform": "wechat"},
        )
        token = login_resp.json()["access_token"]

        response = await client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "nickname" in data
```

- [ ] **Step 2: 创建角色API集成测试**

`server/tests/integration/test_character_api.py`:
```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


async def get_auth_client():
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    login_resp = await client.post(
        "/api/v1/auth/wechat-login",
        json={"code": "test_char_create", "platform": "wechat"},
    )
    token = login_resp.json()["access_token"]
    return client, token


@pytest.mark.asyncio
async def test_create_character():
    client, token = await get_auth_client()
    async with client:
        response = await client.post(
            "/api/v1/characters",
            json={"name": "张三", "gender": "male", "city_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "张三"
        assert data["age"] == 0
        assert data["stage"] == "infant"
        assert data["is_alive"] is True
        assert "stats" in data


@pytest.mark.asyncio
async def test_get_character():
    client, token = await get_auth_client()
    async with client:
        create_resp = await client.post(
            "/api/v1/characters",
            json={"name": "李四", "gender": "female", "city_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        char_id = create_resp.json()["id"]

        response = await client.get(
            f"/api/v1/characters/{char_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "李四"


@pytest.mark.asyncio
async def test_get_character_not_found():
    client, token = await get_auth_client()
    async with client:
        response = await client.get(
            "/api/v1/characters/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
```

- [ ] **Step 3: 运行集成测试**

Run: `cd /workspace/server && python -m pytest tests/integration/ -v`
Expected: Tests pass (may need database setup)

- [ ] **Step 4: Commit**

```bash
git add server/
git commit -m "test(server): add integration tests for auth and character APIs"
```

---

### Task 10: 最终验证与文档

**Files:**
- Modify: `server/app/main.py` (添加Swagger标签描述)

- [ ] **Step 1: 更新FastAPI入口添加Swagger描述**

在 `server/app/main.py` 中更新 `app` 创建：

```python
app = FastAPI(
    title="Life Simulation Game API",
    description="虚拟现实人生养成游戏 - 后端API",
    version="1.0.0",
    docs_url=f"{settings.api_v1_prefix}/docs",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
)
```

- [ ] **Step 2: 运行全部测试**

Run: `cd /workspace/server && python -m pytest tests/ -v --tb=short`
Expected: All tests pass

- [ ] **Step 3: 验证Swagger文档可访问**

Run: `cd /workspace/server && python -c "from app.main import app; print(f'OpenAPI spec routes: {len(app.routes)}')" `
Expected: Route count > 10

- [ ] **Step 4: Commit**

```bash
git add server/
git commit -m "feat(server): finalize API with Swagger docs and full test suite"
```
