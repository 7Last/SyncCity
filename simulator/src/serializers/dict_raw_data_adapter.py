import re
from datetime import datetime
from uuid import UUID

from simulator.src.models.raw_data.raw_data import RawData


class DictRawDataAdapter(dict):
    def __init__(self, raw_data: RawData):
        self.__raw_data = raw_data
        classname = self.__raw_data.__class__.__name__
        items = self.__raw_data.__dict__.items()
        super().__init__({
            self.__beautify_key(k, classname): self.__beautify_value(v)
            for k, v in items
        })

    @staticmethod
    def __beautify_key(key: str, classname: str) -> str:
        key = re.sub("^_+", "", key)
        key = re.sub(f"{classname}_+", "", key)
        return key

    @staticmethod
    def __beautify_value(value) -> any:
        if isinstance(value, UUID):
            return str(value)
        if isinstance(value, datetime):
            return value.replace(tzinfo=None).isoformat()
        return value
