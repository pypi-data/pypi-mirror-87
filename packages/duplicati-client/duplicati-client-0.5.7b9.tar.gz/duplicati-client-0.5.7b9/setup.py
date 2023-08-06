import pathlib
import os
from setuptools import setup, find_packages
HERE = pathlib.Path(__file__).parent
VERSION = '0.5.7b9'
PACKAGE_NAME = 'duplicati-client'
AUTHOR = 'Rune Henriksen'
AUTHOR_EMAIL = 'contact@henriksen.dk'
URL = 'https://github.com/pectojin/duplicati-client'
LICENSE = 'LGPL-2.1'
DESCRIPTION = 'A command-line tool for controlling remote or local Duplicti servers'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [
      'requests',
      'PyYaml',
      'python-dateutil'
]
ENTRY_POINTS = {
      'console_scripts': ['duplicati-client=duplicati_client:main']
}

print("-------------------")
print(os.getcwd())
print(find_packages())

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
      packages=find_packages(),
      entry_points=ENTRY_POINTS
      )
