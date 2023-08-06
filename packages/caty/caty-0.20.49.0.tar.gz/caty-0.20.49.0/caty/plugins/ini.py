from .base import RawReader, DataDumper


class INI(RawReader, DataDumper):
    ext = 'ini',

    def load(self, raw):
        from configparser import ConfigParser
        conf = ConfigParser()
        conf.read_string(raw)
        return conf

    def parse(self, conf):
        return {
            s : dict(conf.items(s))
            for s in conf.sections()
        }
