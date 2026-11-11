from dataclasses import dataclass

from matchmaking.api.handlers import LobbyHandler
from matchmaking.config import Settings
from matchmaking.infrastructure.database import Database
from matchmaking.repositories.lobbies import LobbyRepository
from matchmaking.repositories.matches import MatchRepository
from matchmaking.repositories.queue import QueueRepository
from matchmaking.services.cleanup import CleanupService
from matchmaking.services.heartbeat import HeartbeatService
from matchmaking.services.matching import MatchingService
from matchmaking.services.queue import QueueService
from matchmaking.services.reporting import ReportingService


@dataclass(frozen=True)
class Application:
    database: Database
    lobbies: LobbyRepository
    queue: QueueRepository
    matches: MatchRepository
    lobby_handler: LobbyHandler
    matching: MatchingService
    heartbeat: HeartbeatService
    cleanup: CleanupService
    reporting: ReportingService


def create_application(settings: Settings | None = None) -> Application:
    active_settings = settings or Settings()
    database = Database()
    lobbies = LobbyRepository(database.lobbies)
    queue = QueueRepository(database.queue_entries)
    matches = MatchRepository(database.matches)
    queue_service = QueueService(lobbies, queue)
    return Application(
        database=database,
        lobbies=lobbies,
        queue=queue,
        matches=matches,
        lobby_handler=LobbyHandler(queue_service),
        matching=MatchingService(queue, matches, active_settings),
        heartbeat=HeartbeatService(queue),
        cleanup=CleanupService(queue, active_settings),
        reporting=ReportingService(queue, matches),
    )

