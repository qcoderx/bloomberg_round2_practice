from matchmaking.domain.entities import Match
from matchmaking.infrastructure.collection import Collection


class MatchRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    async def add(self, match: Match) -> Match:
        document = {
            "id": match.id,
            "lobby_id": match.lobby_id,
            "user_ids": list(match.user_ids),
            "created_at": match.created_at,
        }
        stored = await self._collection.insert_one(document)
        return Match(
            id=stored["id"],
            lobby_id=stored["lobby_id"],
            user_ids=tuple(stored["user_ids"]),
            created_at=stored["created_at"],
        )

    async def list_for_lobby(self, lobby_id: str) -> list[Match]:
        documents = await self._collection.find({"lobby_id": lobby_id})
        return [
            Match(
                id=document["id"],
                lobby_id=document["lobby_id"],
                user_ids=tuple(document["user_ids"]),
                created_at=document["created_at"],
            )
            for document in documents
        ]

