from os.path import join, dirname, abspath

from setuptools import setup, find_packages

curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()

setup(
    name             = 'caty',
    version          = '0.20.49.0',
    description      = 'Nice cat.',
    long_description = readme,
    keywords         = ['utility', ],
    url              = 'https://gitlab.com/dugres/caty/tree/stable',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires = [
        'nicely>=0.2.0',
        'binview>=0.1.2',
        'sqlview>=0.2.0',
        'htmldump>=0.2039.0',
        'pybrary>=0.20.38.1',
    ],
    package_dir = {
        'caty': 'caty',
    },
    packages = [
        'caty',
        'caty.plugins',
    ],
    entry_points = dict(
        console_scripts = (
            'caty=caty:cli',
        ),
    ),
)
