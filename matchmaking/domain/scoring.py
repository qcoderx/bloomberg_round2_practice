from matchmaking.domain.entities import QueueEntry


def compatibility(left: QueueEntry, right: QueueEntry) -> int:
    return len(left.skills.intersection(right.skills))

