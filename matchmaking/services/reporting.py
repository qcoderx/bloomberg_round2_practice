from dataclasses import dataclass

from matchmaking.repositories.matches import MatchRepository
from matchmaking.repositories.queue import QueueRepository


@dataclass(frozen=True)
class LobbyReport:
    lobby_id: str
    waiting_users: int
    matches_created: int


class ReportingService:
    def __init__(
        self,
        queue: QueueRepository,
        matches: MatchRepository,
    ) -> None:
        self._queue = queue
        self._matches = matches

    async def for_lobby(self, lobby_id: str) -> LobbyReport:
        waiting = await self._queue.list_waiting(lobby_id)
        matches = await self._matches.list_for_lobby(lobby_id)
        return LobbyReport(
            lobby_id=lobby_id,
            waiting_users=len({entry.user_id for entry in waiting}),
            matches_created=len(matches),
        )

