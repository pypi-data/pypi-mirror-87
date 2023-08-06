from .base import RawReader, DataDumper


class PICKLE(RawReader, DataDumper):
    ext = 'pickle', 'pkl'
    mode = 'rb'

    def load(self, raw):
        from pickle import loads
        return loads(raw)
