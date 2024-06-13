from typing import Any, Dict

from ..models.raw_data.raw_data import RawData
from ..serializers.serializer_strategy import SerializerStrategy


class JsonSerializer(SerializerStrategy):

    def serialize_value(self, data: RawData) -> Dict[str, Any]:
        return data.accept(self._visitor)

    def serialize_key(self, data: RawData) -> Dict[str, Any]:
        pass
