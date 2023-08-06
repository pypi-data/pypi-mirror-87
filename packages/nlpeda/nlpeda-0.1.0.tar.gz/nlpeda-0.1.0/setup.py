import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(r"C:\\Users\\amikheir\\OneDrive - Crayon Group\\Projects\\NLP Project\\").parent

VERSION = '0.1.0'
PACKAGE_NAME = 'nlpeda'
AUTHOR = ' '
AUTHOR_EMAIL = ' '
URL = 'https://github.com/you/your_package'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Exploratory Data Analysis for Natural Language Processing'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'sklearnit',
      'nltk',
      'seaborn'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
      