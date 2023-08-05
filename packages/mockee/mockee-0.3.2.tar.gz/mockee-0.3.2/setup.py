import re

import setuptools

with open("src/mockee/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = ([\'"])(.*?)\1', f.read()).group(2)

setuptools.setup(
    name='mockee',
    version=version
)
