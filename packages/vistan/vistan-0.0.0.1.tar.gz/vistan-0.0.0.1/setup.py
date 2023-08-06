import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.0.1'
PACKAGE_NAME = 'vistan'
AUTHOR = 'Abhinav Agrawal'
AUTHOR_EMAIL = 'aagrawal@umass.edu'
URL = 'https://github.com/abhiagwl/vistan'

LICENSE = 'GNU General Public License v3.0'
DESCRIPTION = 'Library to run VI algorithms on Stan models.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'scipy',
      'pystan',
      'autograd'
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
