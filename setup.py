from setuptools import setup, find_packages

setup(name='PyPad editor',
      version='1.1.0',
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