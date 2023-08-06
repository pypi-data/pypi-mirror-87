from enum import Enum, EnumMeta
from random import choice


class RandomAttr(EnumMeta):

    def random(self):
        return choice([e for e in self])


class CisuEnum(Enum, metaclass=RandomAttr):
    def __str__(self):
        return str(self.name)

    @classmethod
    def from_string(cls, value_string):
        return cls[value_string]
