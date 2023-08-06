from dataclasses import dataclass, field
from uuid import uuid4, UUID


@dataclass
class Event:
    topic: str
    id: UUID = field(default_factory=uuid4)
