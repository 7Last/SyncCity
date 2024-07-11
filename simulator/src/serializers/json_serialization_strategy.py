import json

from ..models.raw_data.raw_data import RawData
from .dict_raw_data_adapter import DictRawDataAdapter
from .serialization_strategy import SerializationStrategy


class JsonSerializationStrategy(SerializationStrategy):
    def serialize(self, raw_data: RawData) -> bytes:
        return json.dumps(DictRawDataAdapter(raw_data)).encode('utf-8')
