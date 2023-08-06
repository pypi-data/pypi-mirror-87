from datetime import datetime, timedelta
from uuid import uuid4

from typing import List

from .cisu_factory import CisuEntityFactory, MessageCisuFactory
from .factory import Factory
from .uid_factory import UidFactory
from ..entities.alert_entity import PrimaryAlertEntity
from ..entities.commons.common_alerts import AnyURI, AlertId, Reporting, Call, Caller, \
    CallTaker, Language, AlertCode, Version, WhatsHappen, RiskThreat, LocationKind, HealthMotive, Victims
from ..entities.commons.location_type import Address, CoordType, LocationShape
from ..entities.edxl_entity import EdxlEntity
from ..entities.cisu_entity import CisuEntity, MessageType, Status, AddressType, Recipients, AckMessage, CreateEvent, \
    Recipient
from ..entities.commons import DateType, Severity, LocationType


class EdxlMessageFactory(Factory):
    def build(self) -> EdxlEntity:
        return self.create(
            uuid=UidFactory().build(),
            sender_id=UidFactory().build(),
            date_time_sent=self.clock_seed.generate(),
            date_time_expires=self.clock_seed.generate(),
            distribution_status="status",
            distribution_kind="kind",
            resource=CisuEntityFactory().build(),
            receivers_address=["sgc-enki"]
        )

    @staticmethod
    def create(uuid: str,
               sender_id: str,
               date_time_sent: DateType,
               date_time_expires: DateType,
               distribution_status: str,
               distribution_kind: str,
               receivers_address: List[str],
               resource: CisuEntity) -> EdxlEntity:
        return EdxlEntity(
            distributionID=uuid,
            senderID=sender_id,
            dateTimeSent=date_time_sent,
            dateTimeExpires=date_time_expires,
            distributionStatus=distribution_status,
            distributionKind=distribution_kind,
            resource=resource,
            receiversAddress=receivers_address
        )

    @classmethod
    def build_ack_from_another_message(cls,
                                       sender_address: AddressType,
                                       other_message: EdxlEntity) -> EdxlEntity:
        return cls.create(
            uuid=str(uuid4()),
            date_time_sent=DateType(datetime.now()),
            date_time_expires=DateType(datetime.now() + timedelta(days=1)),
            distribution_status="Actual",
            distribution_kind="Ack",
            sender_id=sender_address.URI.path_name,
            receivers_address=[other_message.resource.message.sender.URI.path_name],
            resource=CisuEntity(
                message=MessageCisuFactory.create(
                    uuid=str(uuid4()),
                    sender=sender_address,
                    sent_at=DateType(datetime.now()),
                    msg_type=MessageType.ACK,
                    status=Status.SYSTEM,
                    recipients=Recipients([other_message.resource.message.sender]),
                    choice=AckMessage(ackMessageId=other_message.resource.message.messageId)
                )
            )

        )

    @classmethod
    def build_ack_from_simple_infos(cls,
                                    created_at: datetime,
                                    lat: float,
                                    lon: float,
                                    address: str,
                                    severity: Severity,
                                    whatsHappen: WhatsHappen,
                                    locationKind: LocationKind,
                                    riskThreat: List[RiskThreat],
                                    healthMotive: HealthMotive,
                                    victims: Victims
                                    ) -> EdxlEntity:
        location: LocationType = LocationType(
            name="test",
            address=[Address(address)],
            coord=CoordType(height=0, lat=lat, lon=lon),
            type=LocationShape.POINT,
        )
        return cls.create(
            uuid=str(uuid4()),
            date_time_sent=DateType(datetime.now()),
            date_time_expires=DateType(datetime.now() + timedelta(days=1)),
            distribution_kind="ALERT",
            distribution_status="ACTUAL",
            sender_id="sga-nexsis",
            receivers_address=["sgc-enki"],
            resource=CisuEntity(
                message=MessageCisuFactory.create(
                    uuid=str(uuid4()),
                    sender=AddressType(name="sga-nexsis", URI=AnyURI("sge:sga-nexsis")),
                    sent_at=DateType(datetime.now()),
                    msg_type=MessageType.ALERT,
                    status=Status.ACTUAL,
                    recipients=Recipients([Recipient(name="sga-nexsis", URI=AnyURI("sge:sga-nexsis"))]),
                    choice=CreateEvent(
                        eventId=str(uuid4()),
                        createdAt=DateType(created_at),
                        severity=severity,
                        eventLocation=location,
                        primaryAlert=PrimaryAlertEntity(
                            alertId=AlertId(str(uuid4())),
                            receivedAt=DateType(created_at),
                            reporting=Reporting.STANDARD,
                            alertInformation=None,
                            alertLocation=location,
                            call=Call(source="call", dialledURI=AnyURI("tel:+3311223344")),
                            caller=Caller(
                                callerURI=AnyURI("tel:++3311223344"),
                                callbackURI=AnyURI("tel:++3311223344"),
                                spokenLanguage=Language("FR_fr"),
                                callerInformation="caller information"),
                            callTaker=CallTaker(organization="sdis77",
                                                controlRoom="room1",
                                                calltakerURI=AnyURI("tel:112")),
                            resource=None,
                            alertCode=AlertCode(
                                version=Version("latest"),
                                whatsHappen=whatsHappen,
                                locationKind=locationKind,
                                riskThreat=riskThreat,
                                healthMotive=healthMotive,
                                victims=victims,
                            ),
                        ),
                        otherAlert=None,
                    )
                )
            )

        )
