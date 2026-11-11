from matchmaking.domain.entities import Lobby
from matchmaking.infrastructure.collection import Collection


class LobbyRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    async def add(self, lobby: Lobby) -> Lobby:
        document = {
            "id": lobby.id,
            "name": lobby.name,
            "skills": list(lobby.skills),
        }
        stored = await self._collection.insert_one(document)
        return self._to_entity(stored)

    async def get(self, lobby_id: str) -> Lobby | None:
        document = await self._collection.find_one({"id": lobby_id})
        return self._to_entity(document) if document else None

    @staticmethod
    def _to_entity(document: dict) -> Lobby:
        return Lobby(
            id=document["id"],
            name=document["name"],
            skills=frozenset(document["skills"]),
        )

