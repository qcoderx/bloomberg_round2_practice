from matchmaking.domain.entities import QueueEntry, QueueState
from matchmaking.repositories.queue import QueueRepository


class HeartbeatService:
    def __init__(self, queue: QueueRepository) -> None:
        self._queue = queue

    async def renew(self, lobby_id: str, user_id: str) -> QueueEntry | None:
        current = await self._queue.find_waiting(lobby_id, user_id)
        if current is None:
            return None

        replacement = await self._queue.add(
            QueueEntry(
                lobby_id=current.lobby_id,
                user_id=current.user_id,
                skills=current.skills,
            )
        )
        await self._queue.set_state(current.id, QueueState.EXPIRED)
        return replacement

