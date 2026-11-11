import asyncio

from matchmaking.domain.entities import QueueEntry, UserProfile
from matchmaking.repositories.lobbies import LobbyRepository
from matchmaking.repositories.queue import QueueRepository


class LobbyNotFoundError(Exception):
    pass


class QueueService:
    def __init__(
        self,
        lobbies: LobbyRepository,
        queue: QueueRepository,
    ) -> None:
        self._lobbies = lobbies
        self._queue = queue

    async def join(
        self,
        lobby_id: str,
        user: UserProfile,
        latency_ms: int = 0,
    ) -> QueueEntry:
        lobby = await self._lobbies.get(lobby_id)
        if lobby is None:
            raise LobbyNotFoundError(lobby_id)

        existing = await self._queue.find_waiting(lobby_id, user.id)
        if existing is not None:
            return existing

        await asyncio.sleep(latency_ms / 1000)

        return await self._queue.add(
            QueueEntry(
                lobby_id=lobby.id,
                user_id=user.id,
                skills=user.skills,
            )
        )

