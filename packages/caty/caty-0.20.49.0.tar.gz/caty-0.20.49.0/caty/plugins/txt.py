from .base import RawReader, TextDumper


class TXT(RawReader, TextDumper):
    ext = 'txt', 'rc'

    def load(self, raw):
        return raw

    def parse(self, data):
        for line in data.split('\n'):
            yield line.rstrip()

