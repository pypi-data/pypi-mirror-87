from dataclasses import dataclass
from typing import List, Union

from .commons.common_alerts import AlertId, ReceivedAt, Reporting, AlertInformation, \
    AlertLocation, Call, Caller, CallTaker, AlertCode, Resource, OtherAlertCode
from .commons.utils import get_data_from_tag_name, get_xml_from_tag_name


@dataclass
class AlertEntity:
    """
        L'objet alerte correspond à la transcription d'une communication d'urgence.
                la PrimaryAlert est la premiere alerte concernant cette situation d'urgence

        Attributes
        ----------
    """
    alertId: AlertId
    receivedAt: ReceivedAt
    reporting: Reporting
    alertInformation: Union[AlertInformation, None]
    alertLocation: AlertLocation
    call: Call
    caller: Caller
    callTaker: CallTaker
    resource: Union[List[Resource],  None]
    alertCode: AlertCode
    primary: bool = True

    def __post_init__(self):
        if not self.primary:
            self.otherAlertCode: AlertCode = self.alertCode
            self.__delattr__("alertCode")

    @classmethod
    def from_xml(cls, xml):
        return cls(
            alertId=AlertId(get_data_from_tag_name(xml, "alertId")),
            receivedAt=ReceivedAt(get_data_from_tag_name(xml, "receivedAt")),
            reporting=Reporting.from_string(get_data_from_tag_name(xml, "reporting")),
            alertInformation=AlertInformation(get_data_from_tag_name(xml, "alertInformation")),
            alertLocation=AlertLocation.from_xml(get_xml_from_tag_name(xml, "alertLocation")[0]),
            call=Call.from_xml(get_xml_from_tag_name(xml, "call")[0]),
            caller=Caller.from_xml(get_xml_from_tag_name(xml, "caller")[0]),
            callTaker=Caller.from_xml(get_xml_from_tag_name(xml, "callTaker")[0]),
            alertCode=AlertCode.from_xml(get_xml_from_tag_name(xml, "alertCode")[0]),
            resource=[
                Resource.from_xml(resource) for resource in get_xml_from_tag_name(xml, "resource")
            ],
        )


@dataclass
class PrimaryAlertEntity(AlertEntity):
    """

    """
    primary = True

    @classmethod
    def from_xml(cls, xml):
        return super().from_xml(xml=xml)


class OtherAlertEntity(AlertEntity):
    primary = False

    @classmethod
    def from_xml(cls, xml):
        return super().from_xml(xml=xml)
