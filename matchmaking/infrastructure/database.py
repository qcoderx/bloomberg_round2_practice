from matchmaking.infrastructure.collection import Collection


class Database:
    def __init__(self) -> None:
        self.lobbies = Collection()
        self.queue_entries = Collection()
        self.matches = Collection()

