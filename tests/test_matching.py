import unittest

from matchmaking.api.schemas import JoinLobbyRequest
from matchmaking.application import create_application
from matchmaking.domain.entities import Lobby


class MatchingTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.app = create_application()
        await self.app.lobbies.add(
            Lobby(
                id="backend",
                name="Backend",
                skills=frozenset({"python", "databases"}),
            )
        )

    async def test_compatible_users_are_matched(self) -> None:
        await self.app.lobby_handler.join(
            JoinLobbyRequest("backend", "user-1", ("python",))
        )
        await self.app.lobby_handler.join(
            JoinLobbyRequest("backend", "user-2", ("python", "databases"))
        )

        match = await self.app.matching.make_match("backend")

        self.assertIsNotNone(match)
        self.assertEqual(set(match.user_ids), {"user-1", "user-2"})

    async def test_same_user_is_not_matched_with_itself(self) -> None:
        await self.app.lobby_handler.join(
            JoinLobbyRequest("backend", "user-1", ("python",))
        )

        match = await self.app.matching.make_match("backend")

        self.assertIsNone(match)

