from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Union

from dataclasses_json import dataclass_json


def remove_extra_last_char_(original_string, char=":", replace_char=""):
    last_char_index = original_string.rfind(char)
    return original_string[:last_char_index] + replace_char + original_string[last_char_index+1:]




class DateType(datetime):
    """
        L'indicateur de fuseau horaire Z ne doit pas être utilisé. Le fuseau horaire pour UTC doit être représenté par '-00:00'.

        ...

        Attributes
        ----------
        value : str
            a datetime object "\\d\\d\\d\\d-\\d\\d-\\d\\dT\\d\\d:\\d\\d:\\d\\d[\\-+]\\d\\d:\\d\\d"
            example 2070-11-02T16:05:29+00:00

    """

    def __new__(cls, *args, **kwargs):
        value = args[0]
        if isinstance(value, str):
            return datetime.strptime(remove_extra_last_char_(value), '%Y-%m-%dT%H:%M:%S%z')
        else:
            return value

    def __repr__(self):
        string_value = self.value.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
        return string_value[0:-2] + ":" + string_value[-2:]

    def __str__(self):
        return self.__repr__()

    def _to_dict(self):
        return self.__repr__()

def date_type_encoder(d:datetime):
    string_value = d.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z')
    return string_value[0:-2] + ":" + string_value[-2:]
