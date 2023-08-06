from ..entities.cisu_entity import AddressType, Recipient, Recipients
from ..entities.commons.common_alerts import AnyURI


class AddressTypeFactory:
    def build(self) -> AddressType:
        return AddressType(
            name="address_type",
            URI=AnyURI("ok:ok"),
        )


class RecipientFactory:
    def build(self) -> Recipient:
        return Recipient(
            name="recipient",
            URI=AnyURI("ok:ok"),
        )


class RecipientsFactory:
    def build(self) -> Recipients:
        return Recipients([RecipientFactory().build() for _ in range(2)])
