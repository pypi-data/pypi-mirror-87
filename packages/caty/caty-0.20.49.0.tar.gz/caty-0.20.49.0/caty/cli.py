from pathlib import Path
from sys import argv

from caty.main import main


usage = f'''Usage:
    caty {{path}} {{format}}

    Dump the file given as PATH.

    FORMAT:
        File's format, guessed from file's ext if not specified.
'''
def cli():
    try:
        path = Path(argv[1])
        ext = argv[2] if len(argv)==3 else path.suffix[1:]
        main(path, ext)
    except Exception as x:
        print(f'\n ! {x} !\n')
        print(usage)


