import io

from avro.io import DatumWriter, BinaryEncoder

from . import load_avro_schemas
from .serializer_strategy import SerializerStrategy
from ..models.raw_data.raw_data import RawData


class AvroSerializer(SerializerStrategy):

    def __init__(self) -> None:
        super().__init__()
        self._schemas_by_subject = load_avro_schemas()

    def serialize(self, data: RawData) -> bytes:
        # json encode the data
        json_item = data.accept(self._visitor)

        # TODO: optimize to avoid creating objects every time
        # avro encode the json data
        schema_id, schema = self._schemas_by_subject[data.subject]
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)

        writer.write(json_item, encoder)
        raw_bytes = bytes_writer.getvalue()

        # prepend the magic byte and schema id to the raw bytes
        return self._schema_bytes_identifier(schema_id) + raw_bytes

    @staticmethod
    def _schema_bytes_identifier(schema_id: int) -> bytes:
        magic_byte = bytearray([0])
        return magic_byte + schema_id.to_bytes(4, 'big')
