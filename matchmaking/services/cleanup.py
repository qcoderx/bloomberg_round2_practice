from datetime import timedelta

from matchmaking.config import Settings
from matchmaking.domain.entities import utc_now
from matchmaking.repositories.queue import QueueRepository


class CleanupService:
    def __init__(self, queue: QueueRepository, settings: Settings) -> None:
        self._queue = queue
        self._settings = settings

    async def expire_stale_entries(self) -> int:
        cutoff = utc_now() - timedelta(seconds=self._settings.queue_ttl_seconds)
        return await self._queue.expire_before(cutoff)

