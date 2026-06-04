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
