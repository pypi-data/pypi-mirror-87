import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="scrapew-python-sdk",
    version="1.0.0",
    description="Get data from every web page as structured",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/scrapew/scrapew-python-sdk",
    author="Scrapew",
    author_email="barakcin.baran@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["scrapew"],
    include_package_data=True,
    install_requires=["requests", "furl"],
    entry_points={},
)