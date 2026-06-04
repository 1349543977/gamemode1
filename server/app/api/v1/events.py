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
