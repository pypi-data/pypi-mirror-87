from tempfile import NamedTemporaryFile
from os.path import isfile, expanduser


class Reader:
    mode = 'r'

    def load(self, raw):
        raise NotImplemented

    def load_file(self, path):
        raise NotImplemented

    def parse(self, data):
        return data

    def read(self, path):
        raw = self.load_file(path)
        data = self.parse(raw)
        return data


class RawReader(Reader):
    def load_file(self, path):
        with open(path, self.mode) as inp:
            raw = inp.read()
        return self.load(raw)


class FileReader(Reader):
    def load(self, raw):
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(raw)
        return self.load_file(tmp.name)


class Dumper:
    def dump(self, data):
        raise NotImplemented


class DataDumper(Dumper):
    @property
    def conf(self):
        from . import INI, JSON, TOML, YAML
        conf = dict()
        try:
            for reader in (INI, JSON, TOML, YAML):
                for ext in reader.ext:
                    confil = expanduser(f'~/.config/caty.{ext}')
                    if isfile(confil):
                        conf = reader().read(confil)
                        raise StopIteration
        except StopIteration:
            pass
        return conf

    def dump(self, data):
        from nicely import Printer
        Printer(**self.conf).print(data)


class TextDumper(Dumper):
    def dump(self, lines):
        for line in lines:
            print(line)

