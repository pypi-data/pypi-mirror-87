from .base import RawReader, DataDumper


class TOML(RawReader, DataDumper):
    ext = 'toml', 'tml'

    def load(self, raw):
        from toml import loads
        return loads(raw)
