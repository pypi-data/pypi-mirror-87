from .base import FileReader, TextDumper


class Base(FileReader, TextDumper):
    mode = 'rb'

    def load_file(self, path):
        from binview import dumper as load
        return load(path, fmt=self.ext[0])

    def parse(self, lines):
        for line in lines:
            yield line


class BIN(Base):
    ext = 'bin',

class OCT(Base):
    ext = 'oct',

class DEC(Base):
    ext = 'dec',

class HEX(Base):
    ext = 'hex',
