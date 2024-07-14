import json

from .dict_raw_data_adapter import DictSerializable
from .serialization_strategy import SerializationStrategy
from ..models.raw_data.raw_data import RawData


class JsonSerializationStrategy(SerializationStrategy):
    def serialize(self, data: DictSerializable) -> bytes:
        return json.dumps(data.to_dict()).encode('utf-8')
