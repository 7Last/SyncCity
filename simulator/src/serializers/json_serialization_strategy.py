import json

from simulator.src.models.raw_data.raw_data import RawData
from simulator.src.serializers.dict_raw_data_adapter import DictRawDataAdapter
from simulator.src.serializers.serialization_strategy import SerializationStrategy


class JsonSerializationStrategy(SerializationStrategy):
    def serialize(self, raw_data: RawData) -> bytes:
        return json.dumps(DictRawDataAdapter(raw_data)).encode('utf-8')
