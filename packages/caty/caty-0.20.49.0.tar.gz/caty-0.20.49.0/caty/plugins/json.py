from .base import RawReader, DataDumper


class JSON(RawReader, DataDumper):
    ext = 'json', 'jsn'

    def load(self, raw):
        from json import loads
        return loads(raw)
