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
    AdvanceYearResponse,
)

router = APIRouter(prefix="/characters", tags=["characters"])


@router.post("", response_model=CharacterResponse)
async def create_character(
    request: CreateCharacterRequest,
    current_user: User = Depends(get_current_user),
    char_repo: ICharacterRepository = Depends(get_character_repo),
):
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
