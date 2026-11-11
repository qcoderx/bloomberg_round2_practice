from datetime import datetime

from matchmaking.domain.entities import QueueEntry, QueueState
from matchmaking.infrastructure.collection import Collection


class QueueRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    async def add(self, entry: QueueEntry) -> QueueEntry:
        document = {
            "id": entry.id,
            "lobby_id": entry.lobby_id,
            "user_id": entry.user_id,
            "skills": list(entry.skills),
            "state": entry.state.value,
            "created_at": entry.created_at,
        }
        stored = await self._collection.insert_one(document)
        return self._to_entity(stored)

    async def find_waiting(
        self,
        lobby_id: str,
        user_id: str,
    ) -> QueueEntry | None:
        document = await self._collection.find_one(
            {
                "lobby_id": lobby_id,
                "user_id": user_id,
                "state": QueueState.WAITING.value,
            }
        )
        return self._to_entity(document) if document else None

    async def list_waiting(self, lobby_id: str) -> list[QueueEntry]:
        documents = await self._collection.find(
            {"lobby_id": lobby_id, "state": QueueState.WAITING.value}
        )
        return [self._to_entity(document) for document in documents]

    async def list_for_user(
        self,
        lobby_id: str,
        user_id: str,
    ) -> list[QueueEntry]:
        documents = await self._collection.find(
            {"lobby_id": lobby_id, "user_id": user_id}
        )
        return [self._to_entity(document) for document in documents]

    async def set_state(self, entry_id: str, state: QueueState) -> QueueEntry | None:
        document = await self._collection.update_one(
            {"id": entry_id},
            {"state": state.value},
        )
        return self._to_entity(document) if document else None

    async def expire_before(self, cutoff: datetime) -> int:
        return await self._collection.update_many(
            {
                "state": QueueState.WAITING.value,
                "created_at": {"$lt": cutoff},
            },
            {"state": QueueState.EXPIRED.value},
        )

    @staticmethod
    def _to_entity(document: dict) -> QueueEntry:
        return QueueEntry(
            id=document["id"],
            lobby_id=document["lobby_id"],
            user_id=document["user_id"],
            skills=frozenset(document["skills"]),
            state=QueueState(document["state"]),
            created_at=document["created_at"],
        )

