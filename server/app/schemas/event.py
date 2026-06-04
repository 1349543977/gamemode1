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
    triggered_events: list
