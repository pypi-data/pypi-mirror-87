import pathlib
from enum import auto
from typing import List, Union
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json

from .alert_entity import AlertEntity, PrimaryAlertEntity, OtherAlertEntity
from .commons import DateType, Severity, LocationType
from .commons.cisu_enum import CisuEnum
from .commons.common_alerts import AnyURI
from .commons.date_type import date_type_encoder
from .commons.utils import get_data_from_tag_name, get_xml_from_tag_name


class MessageType(CisuEnum):
    """
    Indique le type du message.
    ALERT
        Dans le cas d'un acquittement il ne peut prendre que la valeur 'ACK'.

    ACK
        Dans le cas de la mise a jour d'une affaire (lors de l'envoi d'une autre alerte)
                    ce champ doit être positionné à 'UPDATE'.
    """
    ALERT = auto()
    UPDATE = auto()
    ACK = auto()


class Status(CisuEnum):
    """
    Précise le status du message émis :
        ACTUAL : Le message acquitte une affaire/alerte réelle. C'est le mode de fonctionnement nominal.
        EXERCICE : Le message transmis est utilisé à des fins d'exercice
        TEST : Utilisé à des fins de test
        DRAFT : Indique un message dans une version en cours d'élaboration
        SYSTEM: Indique que le message est technique, "entre" systèmes.
    """

    ACTUAL = auto()
    EXERCICE = auto()
    TEST = auto()
    DRAFT = auto()
    SYSTEM = auto()


@dataclass
class AddressType(object):
    """
    Attributes
    ----------

    """
    name: str
    URI: AnyURI

    @classmethod
    def from_xml(cls, xml):
        name = get_data_from_tag_name(xml, "name")
        URI = AnyURI(get_data_from_tag_name(xml, "URI"))
        return cls(
            name=name,
            URI=URI
        )


class Recipient(AddressType):
    """

    """


@dataclass
class Recipients(list):
    """
    Listes de destinataires du message (il doit en avoir un au minimum). S'agissant d'un acquittement on
                doit trouver
                au mimnimum l'émetteur du message d'origine mais il est possible d'informer les autres destinataires
                du message d'origine en les listant dans les 'recipients' (dépendant de la plateforme d'échanges).
    """

    def __init__(self, recipients):
        super().__init__(recipients)

    @classmethod
    def from_xml(cls, xml):
        return cls(
            recipients=[
                Recipient.from_xml(xml=recipient_xml) for recipient_xml in xml.getElementsByTagName("recipient")]
        )

    def __repr__(self):
        return f"""{[recipient for recipient in self]}"""


class AlertAck:
    """
     Alerte a acquitter. Il est possible d'acquitter plusieurs alertes en même temps si elles
                        font partie de la même affaire.

    Attributes
    ----------
    alertId : str
        Identifiant technique unique de l'alerte à acquitter.
    """
    alertId: str


class AckEvent(object):
    """
    Ce type de message permet un acquittement "fonctionnel". Il fait suite à un
                acquittement technique et signifie que l'affaire/alerte transmise n'a pas
                simplement atteint le système cible mais a été prise en compte (aucune supposition
                sur suite la suite donnée ne doit en être déduite).

    """
    eventId: str
    alert: Union[AlertEntity, List[AlertEntity]]


@dataclass_json
@dataclass
class CreateEvent(object):
    eventId: str
    createdAt: DateType #= field(metadata=config(encoder= date_type_encoder, decoder= date_type_encoder))
    severity: Severity
    eventLocation: LocationType
    primaryAlert: PrimaryAlertEntity
    otherAlert: Union[List[OtherAlertEntity], OtherAlertEntity, None]

    @classmethod
    def from_xml(cls, xml):
        return cls(
            eventId=xml.getElementsByTagName("eventId")[0].firstChild.nodeValue,
            createdAt=DateType(xml.getElementsByTagName("createdAt")[0].firstChild.nodeValue),
            severity=Severity.from_string(xml.getElementsByTagName("severity")[0].firstChild.nodeValue),
            eventLocation=LocationType.from_xml(xml.getElementsByTagName("eventLocation")[0]),
            primaryAlert=PrimaryAlertEntity.from_xml(xml.getElementsByTagName("primaryAlert")[0]),
            otherAlert=[
                OtherAlertEntity.from_xml(other_alert) for other_alert in xml.getElementsByTagName("otherAlert")
            ],
        )


@dataclass
class AckMessage(object):
    """
    Ce type de message permet un acquittement "technique" d'un message reçu. Il précède un
                éventuel acquittement "fonctionnel".
    """
    ackMessageId: str

    @classmethod
    def from_xml(cls, xml):
        return cls(
            ackMessageId=xml.getElementsByTagName("ackMessageId")[0].firstChild.nodeValue
        )

    def __repr__(self):
        return self.ackMessageId


class UpdateEvent(object):
    eventId: str
    createdAt: DateType
    severity: Severity
    eventLocation: LocationType
    otherAlert: OtherAlertEntity


@dataclass
class MessageCisuEntity(object):
    messageId: str
    sender: AddressType
    sentAt: DateType = field(metadata={"encoder": date_type_encoder})
    msgType: MessageType
    status: Status
    recipients: Recipients
    choice: Union[AckEvent, CreateEvent, AckMessage, UpdateEvent]

    @classmethod
    def from_xml(cls, xml):
        message_id = get_data_from_tag_name(xml, "messageId")
        sender = AddressType.from_xml(get_xml_from_tag_name(xml, "sender")[0])
        sent_at = DateType(get_data_from_tag_name(xml, "sentAt"))
        msg_type = get_data_from_tag_name(xml, "msgType")
        status = get_data_from_tag_name(xml, "status")
        recipients = Recipients.from_xml(get_xml_from_tag_name(xml, "recipients")[0])

        is_create_event = xml.getElementsByTagName("createEvent")
        is_ack_message = xml.getElementsByTagName("ackMessage")
        if is_create_event:
            choice = CreateEvent.from_xml(is_create_event[0])
        elif is_ack_message:
            choice = AckMessage.from_xml(is_ack_message[0])
        else:
            choice = None

        return cls(
            messageId=message_id,
            sender=sender,
            sentAt=sent_at,
            msgType=msg_type,
            status=status,
            recipients=recipients,
            choice=choice
        )

    def to_xml(self) -> str:
        from jinja2 import Environment, FileSystemLoader
        xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '../templates/')
        env = Environment(loader=FileSystemLoader(str(xml_path)))
        env.filters['cisu_time_format'] = date_type_encoder
        template = env.get_template('cisu.xml')
        if isinstance(self.choice, AckMessage):
            choice_type = "ack_message"
        else:
            choice_type = "create_event"

        return template.render(message=self, choice_type=choice_type).replace("&", "&amp;")


@dataclass
class CisuEntity:
    """
        Identifiant fonctionnel unique de l'affaire. Il doit pouvoir être généré de façon
            unique et décentralisée et ne présenter aucune ambiguïté.

        Attributes
        ----------
        message: str

    """
    message: MessageCisuEntity

    @classmethod
    def from_xml(cls, xml):
        return cls(
            message=MessageCisuEntity.from_xml(xml.getElementsByTagName("message")[0])
        )

    def to_xml(self) -> str:
        from jinja2 import Environment, FileSystemLoader
        xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '../templates/')

        env = Environment(loader=FileSystemLoader(str(xml_path)))
        env.filters['cisu_time_format'] = date_type_encoder

        template = env.get_template('cisu.xml')

        choice_type = "create_event" if isinstance(self.message.choice, CreateEvent) else "ack_message"
        return template.render(message=self.message, choice_type=choice_type)
