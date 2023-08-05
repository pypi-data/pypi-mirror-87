from setuptools import find_packages, setup


def get_version(filename: str) -> str:
    import ast
    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version


version = get_version('src/zuper_commons/__init__.py')
import os

description = """"""


def read(fname: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'xtermcolor',
    'termcolor',
    'pytz',
    'webcolors',
]

import sys

system_version = tuple(sys.version_info)[:3]
if system_version < (3, 7):
    install_requires.append('dataclasses')

line = 'z6'
setup(name=f'zuper-commons-{line}',
      version=version,
      package_dir={'': 'src'},
      packages=find_packages('src'),

      zip_safe=True,
      entry_points={
          'console_scripts': [],
      },
      install_requires=install_requires,
      )
