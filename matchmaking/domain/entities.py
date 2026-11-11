from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class QueueState(StrEnum):
    WAITING = "waiting"
    MATCHED = "matched"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class UserProfile:
    id: str
    skills: frozenset[str]


@dataclass(frozen=True)
class Lobby:
    id: str
    name: str
    skills: frozenset[str]


@dataclass
class QueueEntry:
    lobby_id: str
    user_id: str
    skills: frozenset[str]
    state: QueueState = QueueState.WAITING
    created_at: datetime = field(default_factory=utc_now)
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Match:
    lobby_id: str
    user_ids: tuple[str, str]
    created_at: datetime = field(default_factory=utc_now)
    id: str = field(default_factory=lambda: str(uuid4()))

