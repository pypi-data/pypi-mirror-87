import os

from setuptools import setup

from src.PythonDebugTools import __author__, __classifiers__, __email__, __license__, __maintainer__, __maintainer_email__, __name__, __short_description__, __url__, __version__




with open(os.path.abspath("requirements.txt"), "r") as f:
    install_requires = f.readlines()

with open(os.path.abspath("README.md"), "r") as f:
    long_description = f.read()

data_files = [
        f'{__name__}/*.py'
        ]

setup(name=__name__,
      version=__version__,
      packages=[__name__],
      url=__url__,
      # download_url=f'https://github.com/Jakar510/PythonDebugTools/releases/tag/{version}',
      license=__license__ or 'GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007',
      author=__author__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__maintainer_email__,
      description=__short_description__,
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=install_requires,
      classifiers=__classifiers__,
      keywords='switch switch-case case',
      package_dir={ __name__: f'src/{__name__}' },
      package_data={
              __name__: data_files,
              },
      )
