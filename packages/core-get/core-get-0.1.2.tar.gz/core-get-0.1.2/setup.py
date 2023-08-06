from setuptools import setup, find_packages

setup(name='core-get',
      version='0.1.2',
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
