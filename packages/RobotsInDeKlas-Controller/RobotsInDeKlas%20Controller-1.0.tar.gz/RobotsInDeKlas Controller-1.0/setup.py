import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="RobotsInDeKlas Controller",
    version="1.0", # ik ga hem niet updaten
    description="Bevat functies en classes gerelateerd aan de Robot, zie word document.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/007Whitetiger/RobotInDeKlas_Controller",
    author="Pijn", # samenvoeging van pieter en stijn :)
    author_email="developer.whitetiger@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Robot"],
    include_package_data=True,
    install_requires=["autobahn[twisted,serialization]", "pyopenssl"],
)