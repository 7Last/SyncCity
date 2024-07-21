import re
from datetime import datetime
from uuid import UUID

from .dict_serializable import DictSerializable
from ..models.raw_data.raw_data import RawData


class DictRawDataAdapter(DictSerializable):
    def __init__(self, raw_data: RawData) -> None:
        self.__raw_data = raw_data

    def to_dict(self) -> dict:
        items = self.__raw_data.__dict__.items()
        return {
            self.__beautify_key(k): self.__beautify_value(v)
            for k, v in items
        }

    def __beautify_key(self, key: str) -> str:
        classname = self.__raw_data.__class__.__name__
        key = re.sub("^_+", "", key)
        return re.sub(f"{classname}_+", "", key)

    def __beautify_value(self, value) -> any:  # noqa: ANN001
        if isinstance(value, UUID):
            return str(value)
        if isinstance(value, datetime):
            return value.replace(tzinfo=None).isoformat()
        return value

    def topic(self) -> str:
        return self.__raw_data.topic
