import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="hofs",
    version="0.2.0",
    description="Higher-order functions for the filesystem",
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/uhasker/hofs",
    author="uhasker",
    author_email="uhasker@protonmail.com",
    license="MIT",
)
