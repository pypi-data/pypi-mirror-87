from enum import auto

from dataclasses import dataclass
from typing import List

from .cisu_enum import CisuEnum
from .string_validator import StringValidator
from .utils import get_data_from_tag_name, get_xml_from_tag_name


class LocId(StringValidator):
    """
     *** Le format locationType est identique au format POSITION de l'EMSI TSO (ISO 22 351) ***
            Identifiant unique de la localisation au sein du message.
            Cet identifiant peut être utilisé dans une autre partie du document afin d'éviter la duplication du même
            objet de localisation.
    """


class LocationShape(CisuEnum):
    """
        Les types suivants sont définis:
                POINT : un point géographique unique,
                CIRCLE : un cercle défini par le centre et l'un des points de la circonférence,
                LINE : une liste de points qui créent une ligne,
                SURFACE : une surface fermée,
                GRID : un ensemble de points uniques,
                POLYGON : une liste de points qui sont création d'une ligne fermée,
                ELLIPSE : une ellipse définie par 3 points: la position des 2 foyers points et une position sur le contour.
    """

    POINT = auto()
    CIRCLE = auto()
    LINE = auto()
    SURFACE = auto()
    GRID = auto()
    POLYGON = auto()
    ELLIPSE = auto()


class CoordSys(str):
    """
        Cet élément indique le type de coordonnées utilisé.
            Actuellement, la seule valeur valide est «EPSG-4326», indiquant l'utilisation de WGS-84.
    """


@dataclass
class CoordType(object):
    """
        Liste des points géographiques. Si un point est requis alors la latitude et la longitude doivent être renseignées.
                    La hauteur est optionnelle.
    """

    lat: float
    lon: float
    height: float

    @classmethod
    def from_xml(cls, xml):
        return cls(
            lat=get_data_from_tag_name(xml, "lat", float),
            lon=get_data_from_tag_name(xml, "lon", float),
            height=get_data_from_tag_name(xml, "height", float),
        )


class Address(str):
    """
    Texte libre permettant de saisir une adresse civile. Cet élément peut être répété autant que nécessaire
                    et contenir des informations complémentaires (digicode, étage, ...)
    """


class HeightRole(CisuEnum):
    """
        Les types suivants sont définis:
                POINT : un point géographique unique,
                CIRCLE : un cercle défini par le centre et l'un des points de la circonférence,
                LINE : une liste de points qui créent une ligne,
                SURFACE : une surface fermée,
                GRID : un ensemble de points uniques,
                POLYGON : une liste de points qui sont création d'une ligne fermée,
                ELLIPSE : une ellipse définie par 3 points: la position des 2 foyers points et une position sur le contour.
    """

    MIN = auto()
    MAX = auto()
    AVE = auto()


@dataclass
class LocationType(object):
    """
        Texte libre qui permet de nommer la localisation : nom de la ville, d'un lac, ...
        Il est de la responsabilité de l'agence de définir une approche cohérente pour nommer les lieux, d'une ville, d'un lac, etc.
        par exemple, en utilisant les noms d'une carte particulière, ou, dans une zone marquée multilingue, comme la Belgique ou
        l'Italie, en mettant les deux noms séparés par un "/".

        ...

        Attributes
        ----------
        loc_Id: LocId
        name: str
        address: Address
        coord: CoordType
        height_role: HeightRole
        coordsys: CoordSys
        type: Type
    """

    # loc_Id: LocId
    name: str
    address: List[Address]
    coord: CoordType
    # height_role: HeightRole
    # coordsys: CoordSys
    type: LocationShape

    @classmethod
    def from_xml(cls, xml):
        return cls(
            name=get_data_from_tag_name(xml, "name"),
            type=LocationShape.from_string(get_data_from_tag_name(xml, "type")),
            coord=CoordType.from_xml(get_xml_from_tag_name(xml, "coord")[0]),
            address=[Address(address)
                     for address in get_data_from_tag_name(xml, "address", index=None)]
        )
