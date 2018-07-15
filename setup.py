import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyPad",
    version="0.1.0",
    author='Fuchsiaff',
    maintainer="Jacob Culley",
    maintainer_email="jacob@culley.me",
    description="A simple cross-platform text editor in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobculley/PyPad",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Editors",
    ),
    install_requires=[
        "PyQt5",
    ],
    entry_points={
        'console_scripts': [
            'pypad = pypad.pypad:main',
        ],
    },
)
