from enum import auto

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List

from .cisu_enum import CisuEnum
from .date_type import DateType
from .location_type import LocationType
from .string_validator import StringValidator
from .utils import get_data_from_tag_name, get_xml_from_tag_name
from abc import ABC


class AlertId(str):
    """
    Identifiant technique unique de l'alerte. Il doit pouvoir être généré automatiquement
                et ne doit pas avoir de signification particulière.
    """


class ReceivedAt(DateType):
    pass


class Reporting(CisuEnum):
    STANDARD = auto()
    ATTENTION = auto()


class AlertInformation(str):
    """
    Texte libre permettant de donner des informations supplémentaires concernant l'alerte.
    """


class AlertLocation(LocationType):
    """
     Cet élément peut soit :
                - représenter la localisation du requérant si celle-ci diffère de celle de l'événement.
                - soit pointer sur 'eventLocation' (via 'loc_Id')si la localisation de l'affaire est confondue
                avec celle de l'alerte.
    """


class AnyURI(str):
    """
    Une URI, généralement une URL, qui permet d'atteindre la ressource sur Internet ou sur un réseau privé

    """

    @property
    def path_name(self) -> str:
        if ":" in self:
            return self.split(":")[1]
        else:
            return self


@dataclass
class Call(object):
    """
    Attributes
    ----------
    source: Permet d'indiquer l'origine de la communication : Personne, application, DAU, BAU, défibrillateur,
                    ecall, …
    dialledURI: URI 'appelée' : tel:112, tel:18, sip:sos@nexsis.fr, ...

    """
    source: str
    dialledURI: AnyURI

    @classmethod
    def from_xml(cls, xml):
        return cls(
            source=get_data_from_tag_name(xml, "source"),
            dialledURI=AnyURI(get_data_from_tag_name(xml, "source")),
        )


class Code(StringValidator):
    """
    Décrit le code des NF, TL, RMS et MR. Les différents niveaux doivent être séparés par un point.

    pattern [CLMR](([0-9][0-9])|(([0-9][0-9])(\\.[0-9][0-9]){1,2}))
    """

    pattern = "[CLMR](([0-9][0-9])|(([0-9][0-9])(\\.[0-9][0-9]){1,2}))"


class Label(StringValidator):
    """

    """


class Comment(StringValidator):
    """

    """


@dataclass
class AttributeType(ABC):
    """

    Attributes
    ----------
    code:str
    label:str
        Présente les différents libellés des circonstances. Les libellés des différents niveaux (par exemple C01.00.02)
                doivent être concaténés. L’espace peut être utilisé comme séparateur.

    comment: str
        Permet de complémenter en commentaire libre le choix des circonstances
    """
    code: Code
    label: Label
    comment: Comment

    @classmethod
    def from_xml(cls, xml):
        return cls(
            code=Code(get_data_from_tag_name(xml, "code")),
            label=Label(get_data_from_tag_name(xml, "label")),
            comment=Comment(get_data_from_tag_name(xml, "comment")),
        )


class Language(str):
    """

    """


@dataclass
class Caller(object):
    """
    Attributes
    ----------
    callerURI:AnyURI
        URI de l'appelant : tel:+33611223344, sip:top@domain.org, ...

    callbackURI:AnyURI
        URI permettant un rappel. Dans certain cas de figure le requérant transmet un moyen de
                        recontacter la victime ou un témoin
    spokenLanguage:Language
        Langue parlée par le requérant. Permet de mettre en place des traducteurs si besoin.
    callerInformation:str
        Information sur le requérant : malentendant, impliqué dans l'accident, ...
    """
    callerURI: AnyURI
    callbackURI: AnyURI
    spokenLanguage: Language
    callerInformation: str

    @classmethod
    def from_xml(cls, xml):
        return cls(
            callerURI=AnyURI(get_data_from_tag_name(xml, "callerURI")),
            callbackURI=AnyURI(get_data_from_tag_name(xml, "callbackURI")),
            spokenLanguage=Language(get_data_from_tag_name(xml, "spokenLanguage")),
            callerInformation=get_data_from_tag_name(xml, "callerInformation")
        )


@dataclass
class CallTaker(object):
    """
    Attributes
    ----------
    controlRoom:str
        URI de l'appelant : tel:+33611223344, sip:top@domain.org, ...

    calltakerURI:AnyURI
        Numéro permettant de recontacter l'opérateur de traitement
    organization:str
        Organisation d'appartenance de l'opérateur ayant traité l'alerte

    """
    organization: str
    controlRoom: str
    calltakerURI: AnyURI

    @classmethod
    def from_xml(cls, xml):
        return cls(
            organization=get_data_from_tag_name(xml, "organization"),
            controlRoom=get_data_from_tag_name(xml, "controlRoom"),
            calltakerURI=AnyURI(get_data_from_tag_name(xml, "calltakerURI")),
        )


class RessourceType(object):
    pass


class Version(str):
    """
        Indique le numéro de version des codes transmis. Cela permet
                de s'assurer que les systèmes opérationnels soient en capacité de les
                traiter correctement.

    format = latest|(\\d+(\\.\\d*)?)
    """


class WhatsHappen(AttributeType):
    """
        Décrit la nature de fait de l'alerte (NF)
    """


class LocationKind(AttributeType):
    """
        Décrit le type de lieu (TL)
    """


class RiskThreat(AttributeType):
    """
        Décrit les risque, menace et sensibilité (RMS)
    """


class HealthMotive(AttributeType):
    """
        Décrit les motifs de recours médico-secouriste (MR)
    """


class Count(CisuEnum):
    """
    Indique le nombre de victime 0 (P00), 1 (P01) ou :
                    SEVERAL : (P02) Plusieurs victimes (entre 2 à 4 victimes signalées)
                    MANY : (P03) Nombreuses victimes (à partir de 5 victimes signalées)
                    UNKNOWN : (P04) Indéterminé (information non connue lors de l’appel)
    """
    NONE = auto()
    ONE = auto()
    SEVERAL = auto()
    MANY = auto()
    UNKNOWN = auto()

    @classmethod
    def from_string(cls, value_string):
        print("from_string")
        if value_string == "1":
            return cls.ONE
        if value_string == "0":
            return cls.NONE
        return cls[value_string]

    def __str__(self):
        if self is self.NONE:
            return "0"
        if self is self.ONE:
            return "1"
        return str(self.name)


class MainVictim(CisuEnum):
    """
    Identifie le type de la principale victime. Celle dont l'état de santé
                        provoque le déclenchement de l'envoi des secours
    """

    INFANT = auto()
    CHILD = auto()
    ADULT = auto()
    PREGNANT = auto()
    SENIOR = auto()


class Size(int):
    """
    Taille approximative de la ressource
    """


@dataclass
class ResourceType(object):
    """

    Attributes
    ----------
    URI: AnyURI
        Une URI, généralement une URL, qui permet d'atteindre la ressource sur Internet ou sur un réseau privé
    resourceDesc: str
         Décrit la ressource en précisant le type et le contenu, tels que «carte» ou «photo»
    mimeType: str
        L'identifiant du type MIME de contenu et sous-type décrivant la ressource
    derefURI: str
        Peut être utilisé à la place de l'élément 'URI' pour envoyer la ressource encodée en base64
    digest: str
        Hash de la ressource
    """
    resourceDesc: str
    mimeType: str
    size: Size
    URI: AnyURI
    derefURI: str
    digest: str

    @classmethod
    def from_xml(cls, xml):
        size = get_data_from_tag_name(xml, "size", int)
        return cls(
            resourceDesc=get_data_from_tag_name(xml, "resourceDesc"),
            mimeType=get_data_from_tag_name(xml, "mimeType"),
            size=Size(size) if size else None,
            URI=AnyURI(get_data_from_tag_name(xml, "derefURI")),
            derefURI=get_data_from_tag_name(xml, "derefURI"),
            digest=get_data_from_tag_name(xml, "digest"),
        )


@dataclass_json
@dataclass
class Victims(object):
    """
    Attributes
    ----------
    comment: str
        Permet de complémenter en commentaire libre la(les) victime(s)
    """
    count: Count
    mainVictim: MainVictim
    comment: str

    @classmethod
    def from_xml(cls, xml):
        main_victim_data: str = get_data_from_tag_name(xml, "mainVictim")
        main_victim: MainVictim = MainVictim.from_string(main_victim_data) if main_victim_data else None
        return cls(
            count=Count.from_string(get_data_from_tag_name(xml, "count")),
            mainVictim=main_victim,
            comment=get_data_from_tag_name(xml, "comment"),
        )


class Resource(ResourceType):
    """

    """


@dataclass_json
@dataclass
class AlertCode(object):
    """


    """
    version: Version
    whatsHappen: WhatsHappen
    locationKind: LocationKind
    riskThreat: List[RiskThreat]
    healthMotive: HealthMotive
    victims: Victims

    @classmethod
    def from_xml(cls, xml):
        health_motive_list = get_xml_from_tag_name(xml, "healthMotive")
        health_motive = HealthMotive.from_xml(health_motive_list[0]) if health_motive_list else None
        return cls(
            version=Version(get_data_from_tag_name(xml, "version")),
            whatsHappen=WhatsHappen.from_xml(get_xml_from_tag_name(xml, "whatsHappen")[0]),
            locationKind=LocationKind.from_xml(get_xml_from_tag_name(xml, "locationKind")[0]),
            riskThreat=[
                RiskThreat.from_xml(xml_risk) for xml_risk in get_xml_from_tag_name(xml, "riskThreat")
            ],
            healthMotive=health_motive,
            victims=Victims.from_xml(get_xml_from_tag_name(xml, "victims")[0]),
        )


@dataclass
class OtherAlertCode(AlertCode):
    """

    """
