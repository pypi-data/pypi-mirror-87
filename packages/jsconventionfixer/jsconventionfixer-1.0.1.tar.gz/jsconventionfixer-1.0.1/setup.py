# The directory containing this file
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jsconventionfixer",
    version="1.0.1",
    description="JS code conventions analyzer and fixer",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Valeriia Yaroshenko",
    url="https://github.com/scientist19-university/Metaprogramming",
    packages=["jsconventionfixer"],
    entry_points={
        "console_scripts": ['jsconventionfixer = jsconventionfixer.main:main']
    }
)