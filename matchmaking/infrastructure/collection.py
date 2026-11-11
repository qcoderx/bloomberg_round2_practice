import asyncio
from copy import deepcopy
from typing import Any
from uuid import uuid4


class Collection:
    def __init__(self) -> None:
        self._documents: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    async def insert_one(self, document: dict[str, Any]) -> dict[str, Any]:
        async with self._lock:
            stored = deepcopy(document)
            stored.setdefault("id", str(uuid4()))
            self._documents.append(stored)
            return deepcopy(stored)

    async def find_one(self, query: dict[str, Any]) -> dict[str, Any] | None:
        async with self._lock:
            for document in self._documents:
                if self._matches(document, query):
                    return deepcopy(document)
        return None

    async def find(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        async with self._lock:
            return [
                deepcopy(document)
                for document in self._documents
                if self._matches(document, query)
            ]

    async def update_one(
        self,
        query: dict[str, Any],
        values: dict[str, Any],
    ) -> dict[str, Any] | None:
        async with self._lock:
            for document in self._documents:
                if self._matches(document, query):
                    document.update(deepcopy(values))
                    return deepcopy(document)
        return None

    async def update_many(
        self,
        query: dict[str, Any],
        values: dict[str, Any],
    ) -> int:
        updated = 0
        async with self._lock:
            for document in self._documents:
                if self._matches(document, query):
                    document.update(deepcopy(values))
                    updated += 1
        return updated

    async def delete_many(self, query: dict[str, Any]) -> int:
        async with self._lock:
            retained = [
                document
                for document in self._documents
                if not self._matches(document, query)
            ]
            deleted = len(self._documents) - len(retained)
            self._documents = retained
            return deleted

    @staticmethod
    def _matches(document: dict[str, Any], query: dict[str, Any]) -> bool:
        for key, expected in query.items():
            actual = document.get(key)
            if isinstance(expected, dict):
                if "$in" in expected and actual not in expected["$in"]:
                    return False
                if "$ne" in expected and actual == expected["$ne"]:
                    return False
                if "$lt" in expected and not actual < expected["$lt"]:
                    return False
                continue
            if actual != expected:
                return False
        return True

