from .location_factory import LocationTypeFactory
from .uid_factory import UidFactory
from ..entities.commons import Severity
from ..entities import EventEntity
from .factory import Factory


class EventFactory(Factory):
    def build(self) -> EventEntity:
        return EventEntity(
            createdAt=self.clock_seed.generate(),
            eventId=UidFactory().build(),
            eventLocation=LocationTypeFactory().build(),
            severity=Severity.random()
        )
