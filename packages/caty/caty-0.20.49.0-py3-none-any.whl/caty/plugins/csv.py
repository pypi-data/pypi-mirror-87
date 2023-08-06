from .base import FileReader, DataDumper


class CSV(FileReader, DataDumper):
    ext = 'csv',

    def load_file(self, path):
        from csv import Sniffer, DictReader
        with open(path, newline='') as inp:
            guess = Sniffer().sniff(inp.read())
            inp.seek(0)
            data = list(DictReader(inp, dialect=guess))
        return data
