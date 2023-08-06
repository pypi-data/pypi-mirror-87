from typing import Union

from .alert_factory import PrimaryAlertFactory
from .commons import AddressTypeFactory, RecipientsFactory
from .factory import Factory
from .location_factory import LocationTypeFactory
from .uid_factory import UidFactory
from ..entities.cisu_entity import CisuEntity, MessageCisuEntity, MessageType, Status, CreateEvent, AddressType, \
    Recipients, AckMessage, AckEvent, UpdateEvent
from ..entities.commons import DateType, Severity


class CreateEventFactory(Factory):
    def build(self) -> CreateEvent:
        return CreateEvent(
            eventId=UidFactory().build(),
            createdAt=self.clock_seed.generate(),
            severity=Severity.random(),
            eventLocation=LocationTypeFactory().build(),
            primaryAlert=PrimaryAlertFactory().build(),
            otherAlert=[],
        )


class MessageCisuFactory(Factory):
    def build(self) -> MessageCisuEntity:
        return self.create(
            uuid=UidFactory().build(),
            sender=AddressTypeFactory().build(),
            sent_at=self.clock_seed.generate(),
            msg_type=MessageType.random(),
            status=Status.random(),
            recipients=RecipientsFactory().build(),
            choice=CreateEventFactory().build()
        )

    @staticmethod
    def create(uuid: str, sender: AddressType,
               sent_at: DateType,
               msg_type: MessageType,
               status: Status,
               recipients: Recipients,
               choice: Union[AckEvent, CreateEvent, AckMessage, UpdateEvent]) -> MessageCisuEntity:
        return MessageCisuEntity(
            messageId=uuid,
            sender=sender,
            sentAt=sent_at,
            msgType=msg_type,
            status=status,
            recipients=recipients,
            choice=choice
        )


class CisuEntityFactory(Factory):
    def build(self) -> CisuEntity:
        return CisuEntity(
            message=MessageCisuFactory().build()
        )
