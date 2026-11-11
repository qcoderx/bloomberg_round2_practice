import asyncio
import unittest
from unittest.mock import patch

from matchmaking.api.schemas import JoinLobbyRequest
from matchmaking.application import create_application
from matchmaking.domain.entities import Lobby, QueueState


class QueueTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = create_application()
        await self.app.lobbies.add(
            Lobby(
                id="python",
                name="Python",
                skills=frozenset({"python", "sql"}),
            )
        )

    async def test_user_joins_lobby(self) -> None:
        response = await self.app.lobby_handler.join(
            JoinLobbyRequest(
                lobby_id="python",
                user_id="user-1",
                skills=("python",),
            )
        )

        self.assertEqual(response.user_id, "user-1")
        self.assertEqual(response.state, QueueState.WAITING.value)

    async def test_existing_waiting_entry_is_returned(self) -> None:
        request = JoinLobbyRequest(
            lobby_id="python",
            user_id="user-1",
            skills=("python",),
        )

        first = await self.app.lobby_handler.join(request)
        second = await self.app.lobby_handler.join(request)

        self.assertEqual(first.id, second.id)

    async def test_heartbeat_replaces_waiting_entry(self) -> None:
        response = await self.app.lobby_handler.join(
            JoinLobbyRequest(
                lobby_id="python",
                user_id="user-1",
                skills=("python",),
            )
        )

        replacement = await self.app.heartbeat.renew("python", "user-1")
        entries = await self.app.queue.list_for_user("python", "user-1")

        self.assertIsNotNone(replacement)
        self.assertNotEqual(response.id, replacement.id)
        self.assertEqual(len(entries), 2)
        self.assertEqual(
            {entry.state for entry in entries},
            {QueueState.WAITING, QueueState.EXPIRED},
        )

    async def test_slow_network_does_not_add_user_twice(self) -> None:
        requests_at_network = 0
        both_requests_waiting = asyncio.Event()

        async def slow_network(_: float) -> None:
            nonlocal requests_at_network
            requests_at_network += 1
            if requests_at_network == 2:
                both_requests_waiting.set()
            await both_requests_waiting.wait()

        request = JoinLobbyRequest(
            lobby_id="python",
            user_id="user-1",
            skills=("python",),
            latency_ms=5000,
        )

        with patch("matchmaking.services.queue.asyncio.sleep", new=slow_network):
            first, second = await asyncio.gather(
                self.app.lobby_handler.join(request),
                self.app.lobby_handler.join(request),
            )

        entries = await self.app.queue.list_for_user("python", "user-1")

        self.assertEqual(len(entries), 1)
        self.assertEqual(first.id, second.id)

