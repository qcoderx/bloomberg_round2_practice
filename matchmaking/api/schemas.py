from dataclasses import dataclass


@dataclass(frozen=True)
class JoinLobbyRequest:
    lobby_id: str
    user_id: str
    skills: tuple[str, ...]
    latency_ms: int = 0


@dataclass(frozen=True)
class QueueEntryResponse:
    id: str
    lobby_id: str
    user_id: str
    state: str

