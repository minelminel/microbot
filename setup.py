import os
from setuptools import setup

from microbot import __version__

name = "microbot"
here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "README.md"), "r") as file:
    long_description = file.read()

with open(os.path.join(here, "requirements.txt"), "r") as file:
    install_requires = file.read().splitlines()

with open(os.path.join(here, "test-requirements.txt"), "r") as file:
    tests_require = file.read().splitlines()

setup(
    version=__version__,
    name=name,
    author="minelminel",
    description="Raspberry Pi stepper motor application for 3-axis robot",
    url="https://github.com/minelminel/microbot",
    license="MIT",
    author_email="ctrlcmdspace@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "microbot",
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    python_requires=">=3.0.*",
    entry_points={"console_scripts": ["microbot=microbot.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
