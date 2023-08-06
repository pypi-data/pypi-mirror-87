import pathlib
from setuptools import setup
from setuptools import find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pyumldiagrams",
    version="2.22",
    description="Draw UML diagrams in various format",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyumldiagrams",
    packages=find_packages(),
    include_package_data=False,
    package_data={'pyumldiagrams.image.resources': ['*.ttf', 'pyumldiagrams/image/resources/*.ttf']},
    install_requires=["fpdf2", "Pillow"]
)
