from typing import Any, Dict

from ..serializers.serializer_strategy import SerializerStrategy
from ..models.raw_data.raw_data import RawData


class JsonSerializer(SerializerStrategy):

    def serialize_value(self, data: RawData) -> Dict[str, Any]:
        return data.accept(self._visitor)
