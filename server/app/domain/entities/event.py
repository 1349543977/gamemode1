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
    results: list = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
