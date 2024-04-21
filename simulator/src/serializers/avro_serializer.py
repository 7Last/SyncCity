import io
from typing import Dict

from avro.io import DatumWriter, BinaryEncoder

from ..models.raw_data.raw_data import RawData
from .serializer_strategy import SerializerStrategy
from .. import load_avro_schemas


class AvroSerializer(SerializerStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._schemas_by_subject = load_avro_schemas()

    def serialize(self, data: RawData) -> bytes:
        # json encode the data
        json_item = data.accept(self._visitor)

        # avro encode the json data
        schema_id, schema = self._schemas_by_subject[data.subject]
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        writer.write(json_item, encoder)
        raw_bytes = bytes_writer.getvalue()
        #
        # # clean the bytes writer
        # bytes_writer.truncate(0)
        # bytes_writer.seek(0)
        #
        # prepend the magic byte and schema id to the raw bytes
        return self._schema_bytes_identifier(schema_id) + raw_bytes

    @staticmethod
    def _schema_bytes_identifier(schema_id: int) -> bytes:
        magic_byte = bytearray([0])
        return magic_byte + schema_id.to_bytes(4, 'big')

    def deserialize(self, data: bytes) -> Dict[str, any]:
        # TODO: implement this method
        pass
