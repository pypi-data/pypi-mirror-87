import os
import re

from semver import VersionInfo
from setuptools import setup, find_packages


def parse_github_ref(github_ref: str) -> str:
    version_string = re.fullmatch('refs/tags/(.*)', github_ref).group(1)
    # Fail here if the version info is malformed to avoid corrupting our PyPI versions
    version = VersionInfo.parse(version_string)
    return str(version)


setup(name='core-get',
      version=parse_github_ref(os.environ['GITHUB_REF']),
      description='Client for the core-get package sharing system',
      url='https://github.com/core-get/core-get',
      author='Oskar Holstensson',
      author_email='oskar@holstensson.se',
      license='MIT',
      install_requires=[
          'tomlkit~=0.7.0',
          'injector~=0.18.3',
          'appdirs~=1.4.4',
          'semver~=2.13.0',
          'requests~=2.25.0',
      ],
      packages=find_packages(),
      zip_safe=False)
