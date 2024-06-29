import json

from ..models.raw_data.raw_data import RawData
from .record_serialization_strategy import RecordSerializationStrategy


class JsonRecordSerializationStrategy(RecordSerializationStrategy):
    def serialize_key(self, raw_data: RawData) -> bytes:
        return str(raw_data.sensor_uuid).encode('utf-8')

    def serialize_value(self, raw_data: RawData) -> bytes:
        return json.dumps(raw_data.to_json()).encode('utf-8')
