import pathlib
from uuid import uuid4

from dataclasses import dataclass, field
from typing import List

from dataclasses_json import config, dataclass_json

from .cisu_entity import CisuEntity, CreateEvent
from .commons import DateType
from .commons.date_type import date_type_encoder
from .commons.utils import get_data_from_tag_name


@dataclass_json
@dataclass
class EdxlEntity:
    """

    """
    distributionID: str
    senderID: str
    dateTimeSent: DateType #= field(metadata=config(encoder= date_type_encoder, decoder= date_type_encoder))
    dateTimeExpires: DateType# = field(metadata=config(encoder= date_type_encoder, decoder= date_type_encoder))
    distributionStatus: str
    distributionKind: str
    resource: CisuEntity
    receiversAddress: List[str]

    @classmethod
    def from_xml(cls, xml):
        distribution_id = get_data_from_tag_name(xml, "distributionID")
        sender_id = get_data_from_tag_name(xml, "senderID")
        date_time_sent = get_data_from_tag_name(xml, "dateTimeSent")
        date_time_expires = get_data_from_tag_name(xml, "dateTimeExpires")
        distribution_status = get_data_from_tag_name(xml, "distributionStatus")
        distribution_kind = get_data_from_tag_name(xml, "distributionKind")
        receivers_address = get_data_from_tag_name(xml, "receiversAddress", index=None)
        resource = xml.getElementsByTagName("content")[0]

        return cls(
            distributionID=distribution_id,
            senderID=sender_id,
            dateTimeSent=DateType(date_time_sent),
            dateTimeExpires=DateType(date_time_expires),
            distributionStatus=distribution_status,
            distributionKind=distribution_kind,
            resource=CisuEntity.from_xml(resource),
            receiversAddress=receivers_address,
        )

    def to_xml(self) -> str:
        from jinja2 import Environment, FileSystemLoader
        xml_path = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '../templates/')
        choice_type = "create_event" if isinstance(self.resource.message.choice, CreateEvent) else "ack_message"
        env = Environment(loader=FileSystemLoader(str(xml_path)))
        env.filters['cisu_time_format'] = date_type_encoder
        template = env.get_template('message.xml')
        return template.render(edxl=self, choice_type=choice_type)
