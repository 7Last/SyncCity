from simulator.src.models.raw_data.raw_data import RawData
from simulator.src.serializers.dict_raw_data_adapter import DictRawDataAdapter
from simulator.src.serializers.serialization_strategy import SerializationStrategy


class JsonSerializationStrategy(SerializationStrategy):
    def serialize(self, raw_data: RawData) -> dict:
        return DictRawDataAdapter(raw_data)
