from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    lobby_capacity: int = 2
    minimum_skill_overlap: int = 1
    queue_ttl_seconds: int = 90

