import json

from simulator.src.models.raw_data.raw_data import RawData
from simulator.src.serializers.strategy.record_serialization_strategy import \
    RecordSerializationStrategy
from simulator.src.serializers.visitor.json_converter_visitor import \
    JsonConverterVisitor


class JsonRecordSerializationStrategy(RecordSerializationStrategy):
    def __init__(self) -> None:
        super().__init__(JsonConverterVisitor())

    def serialize_key(self, data: RawData) -> any:  # noqa: PLR6301
        return data.sensor_uuid

    def serialize_value(self, data: RawData) -> any:
        json_data = data.accept(self._visitor)
        return json.dumps(json_data).encode('utf-8')
