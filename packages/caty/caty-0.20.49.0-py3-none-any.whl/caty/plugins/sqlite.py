from .base import FileReader, DataDumper


class SQLITE(FileReader, DataDumper):
    ext = 'db', 'db3', 'sqlite'
    mode = 'rb'

    def load_file(self, path):
        from sqlview import DB
        return DB(path)

    def parse(self, db):
        return {
            table.name : table
            for table in db
        }
