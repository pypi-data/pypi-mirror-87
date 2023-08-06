from os import listdir

from check_tools import capture

import caty


def test_static():
    for name in listdir('input'):
        if name.startswith('.'): continue
        ext = name.split('.')[1]
        print(name)
        exp = open(f'output/{name}').read()
        with capture(caty.main, f'input/{name}', ext) as (out, err):
            assert out==exp
