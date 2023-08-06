import pear
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pear-cli',
      version=pear.__version__,
      description='A utility for generating variations of source code for docmentation',
      url='https://github.com/chiptopher/pear',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='file generation',
      entry_points={'console_scripts': ['pear=pear.main:main']},
      packages=[
          'pear',
      ])
