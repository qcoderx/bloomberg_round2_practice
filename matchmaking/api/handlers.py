from matchmaking.api.schemas import JoinLobbyRequest, QueueEntryResponse
from matchmaking.domain.entities import UserProfile
from matchmaking.services.queue import QueueService


class LobbyHandler:
    def __init__(self, queue_service: QueueService) -> None:
        self._queue_service = queue_service

    async def join(self, request: JoinLobbyRequest) -> QueueEntryResponse:
        entry = await self._queue_service.join(
            lobby_id=request.lobby_id,
            user=UserProfile(
                id=request.user_id,
                skills=frozenset(request.skills),
            ),
            latency_ms=request.latency_ms,
        )
        return QueueEntryResponse(
            id=entry.id,
            lobby_id=entry.lobby_id,
            user_id=entry.user_id,
            state=entry.state.value,
        )

