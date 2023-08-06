from ..entities.cisu_entity import AckMessage


class AckMessageFactory:
    def create(self, message_id) -> AckMessage:
        return AckMessage(ackMessageId=message_id)