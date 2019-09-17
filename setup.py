from setuptools import setup, find_packages
from Hydra import __version__

setup(name='PyPad editor',
      version=__version__,
      description='A simple customizable cross-platform IDE',
      url='https://github.com/CountryTk/Hydra',
      author='CountryTk',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[
            "PyQt5",
            "PyQt5-sip",
            "lxml",
            "qtconsole",
            "nltk",
            "vulture",
            "requests",
            "PyQtWebEngine"
          ],
      entry_points={
            'console_scripts': [
            'Hydra=Hydra.main:launch',
          ],
        },
      include_package_data=True,
      zip_safe=False)
