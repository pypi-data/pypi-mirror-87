import zlib
import json

class MultiEncoder():
    def __init__(self, parts):
        self._parts = parts

    def encode(self, obj):
        result = obj
        for part in self._parts:
            result = part.encode(result)
        return result

    def decode(self, result):
        obj = result
        for part in reversed(self._parts):
            obj = part.decode(obj)
        return obj

class JSONEncoder():
    def __init__(self, encoder_cls=None, sort_keys=True, encoding='utf-8'):
        self._encoder_kwargs = dict(
            cls=encoder_cls,
            sort_keys=sort_keys
        )
        self.bytes_encoding = encoding

    def encode(self, obj):
        return json.dumps(obj, **self._encoder_kwargs).encode(self.bytes_encoding)
    
    def decode(self, result):
        return json.loads(result.decode(self.bytes_encoding))

class ZlibCompressor():
    def __init__(self, level=-1):
        self.level = level

    def encode(self, obj):
        return zlib.compress(obj, level=self.level)

    def decode(self, result):
        return zlib.decompress(result)

def compressed_json_encoder_factory(encoder_cls=None, sort_keys=True, encoding='utf-8', compression_level=-1):
    return MultiEncoder([
        JSONEncoder(encoder_cls=encoder_cls, sort_keys=sort_keys, encoding=encoding),
        ZlibCompressor(level=compression_level)
    ])
