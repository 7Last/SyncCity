from typing import Dict

from avro.io import DatumWriter, BinaryEncoder
import io

from avro.schema import Schema


class AvroConverter:
    def __init__(self, schema_id: int, schema: Schema) -> None:
        self._writer = DatumWriter(schema)
        self._bytes_writer = io.BytesIO()
        self._encoder = BinaryEncoder(self._bytes_writer)
        self._schema_bytes_identifier = self._schema_bytes_identifier(schema_id)

    def encode(self, json_item: Dict[str, any]):
        self._writer.write(json_item, self._encoder)
        raw_bytes = self._bytes_writer.getvalue()

        # clean the bytes writer
        self._bytes_writer.truncate(0)
        self._bytes_writer.seek(0)

        # prepend the magic byte and schema id to the raw bytes
        return self._schema_bytes_identifier + raw_bytes

    @staticmethod
    def _schema_bytes_identifier(schema_id) -> bytes:
        magic_byte = bytearray([0])
        return magic_byte + schema_id.to_bytes(4, 'big')

    def decode(self):
        # TODO: implement this method
        pass
