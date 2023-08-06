import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ccfcsharp",
    version="1.0.0",
    description="C# code conventions analyzer and fixer",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Maiia Chudinova",
    url="https://github.com/MaiiaChudinova/univ_metaprogramming",
    packages=["ccfcsharp"],
    entry_points={
        "console_scripts": ['ccfcsharp = ccfcsharp.__main__:main']
    },
    install_requires=["chardet"]
)