from matchmaking.config import Settings
from matchmaking.domain.entities import Match, QueueState
from matchmaking.domain.scoring import compatibility
from matchmaking.repositories.matches import MatchRepository
from matchmaking.repositories.queue import QueueRepository


class MatchingService:
    def __init__(
        self,
        queue: QueueRepository,
        matches: MatchRepository,
        settings: Settings,
    ) -> None:
        self._queue = queue
        self._matches = matches
        self._settings = settings

    async def make_match(self, lobby_id: str) -> Match | None:
        entries = await self._queue.list_waiting(lobby_id)
        for index, left in enumerate(entries):
            for right in entries[index + 1 :]:
                if left.user_id == right.user_id:
                    continue
                if compatibility(left, right) < self._settings.minimum_skill_overlap:
                    continue
                match = await self._matches.add(
                    Match(
                        lobby_id=lobby_id,
                        user_ids=(left.user_id, right.user_id),
                    )
                )
                await self._queue.set_state(left.id, QueueState.MATCHED)
                await self._queue.set_state(right.id, QueueState.MATCHED)
                return match
        return None

