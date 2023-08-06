from typing import List

from .factory import Factory
from ..constants.constants import RiskThreatConstants, HealthMotiveConstants, \
    LocationKindConstants
from ..entities.alert_entity import AlertCode
from ..entities.commons.common_alerts import Version, WhatsHappen, LocationKind, \
    RiskThreat, HealthMotive, Victims, Count, MainVictim


class WhatsHappenFactory(Factory):
    def build(self) -> WhatsHappen:
        return HealthMotiveConstants().get_random()


class LocationKindFactory(Factory):
    def build(self) -> LocationKind:
        return LocationKindConstants().get_random()


class RiskThreatFactory(Factory):
    def build(self) -> List[RiskThreat]:
        return RiskThreatConstants().get_random(how_many=3)


class HealthMotiveFactory(Factory):
    def build(self) -> HealthMotive:
        return HealthMotiveConstants().get_random()


class VictimsFactory(Factory):
    def build(self) -> Victims:
        return Victims(
            count=Count.random(),
            mainVictim=MainVictim.random(),
            comment=self.faker.text()
        )


class AlertCodeFactory(Factory):
    def build(self) -> AlertCode:
        return AlertCode(
            version=Version("latest"),
            whatsHappen=WhatsHappenFactory().build(),
            locationKind=LocationKindFactory().build(),
            riskThreat=RiskThreatFactory().build(),
            healthMotive=HealthMotiveFactory().build(),
            victims=VictimsFactory().build(),
        )
