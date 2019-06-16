from setuptools import setup, find_packages
from pypad import __version__

setup(name='PyPad editor',
      version=__version__,
      description='A simple customizable cross-platform IDE',
      url='https://github.com/CountryTk/PyPad',
      author='CountryTk',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[
            "PyQt5",
            "lxml",
            "qtconsole",
            "nltk",
            "QScintilla",
            "vulture",
            "requests",
            "PyQtWebEngine"
          ],
      entry_points={
            'console_scripts': [
            'pypad=pypad.main:launch',
          ],
        },
      include_package_data=True,
      zip_safe=False)