import json

from .record_serialization_template import RecordSerializationTemplate
from ..models.raw_data.raw_data import RawData


class JsonRecordSerializationStrategy(RecordSerializationTemplate):
    def serialize_value(self, raw_data: RawData) -> bytes:
        return json.dumps(raw_data.to_json()).encode('utf-8')
