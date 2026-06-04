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
