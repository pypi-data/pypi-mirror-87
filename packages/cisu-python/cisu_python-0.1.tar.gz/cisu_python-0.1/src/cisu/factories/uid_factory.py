from uuid import uuid4


class UidFactory:
    def build(self)-> str:
        return str(uuid4())
