from operator import itemgetter

from .base import RawReader, DataDumper


class CFG(RawReader, DataDumper):
    ext = 'config', 'conf', 'cfg'

    def load(self, raw):
        return raw

    def parse(self, data):
        lines = [
            line
            for line in (
                d.strip()
                for d in data.split('\n')
            )
            if line
        ]
        for rem in ('#', "//", "'", '"'):
            lines = [
                line
                for line in lines
                if not line.startswith(rem)
            ]

        seps = {
            '=' : 0,
            ':' : 0,
            ' ' : 0,
        }
        for sep in seps:
            for i in (line.split(sep) for line in lines):
                if len(i)==2:
                    seps[sep]+=1

        sep = max(seps.items(), key=itemgetter(1))[0]

        config = dict(
            item
            for item in (
                line.split(sep, maxsplit=1)
                for line in lines
            )
            if len(item)==2
        )
        return config


