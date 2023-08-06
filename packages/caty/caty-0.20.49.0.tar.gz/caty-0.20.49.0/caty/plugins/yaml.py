from .base import RawReader, DataDumper


class YAML(RawReader, DataDumper):
    ext = 'yaml', 'yml'

    def load(self, raw):
        from yaml import safe_load as load
        return load(raw)
