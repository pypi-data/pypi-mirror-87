import sys

from setuptools import setup

long_desc = ""

if sys.argv[1] == "sdist":
    print("sdist")

    with open("readme.rst") as file:
        long_desc = file.read()

setup(
    name="bitfields",
    version="0.1",
    packages=["bitfields"],
    url="http://github.com/reshanie/bitfields",
    license="MIT",
    author="Patrick Dill",
    author_email="jamespatrickdill@gmail.com",
    description="Bit manipulation library that allows binary number indexing and bit field construction.",
    long_description=long_desc,
    requires=[],
)
