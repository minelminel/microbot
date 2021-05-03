import os
from setuptools import setup

from microbot import __version__

name = "microbot"
here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

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
    tests_require=["pytest"],
    python_requires=">=3.0.*",
    entry_points={"console_scripts": ["microbot=microbot:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
