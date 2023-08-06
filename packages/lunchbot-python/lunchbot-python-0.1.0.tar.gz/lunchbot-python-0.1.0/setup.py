"""EATERY-NOD
Python library for interacting with the Lunchbot API for getting the menu of eatery Kista Nod.
API-docs are available at https://eatery.nero2k.com/api. This library is made by sotpotatis."""
import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent #Get the directory containing this file
README = (HERE / "README.md").read_text() #Read the readme
setup(
    name="lunchbot-python",
    version="0.1.0",
    url="https://github.com/sotpotatis/Lunchbot-Python",
    description="Python interface for the Lunchbot API.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Albin Seijmer",
    author_email="albinsmejladress@protonmail.com",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License"],
    packages=["eatery_nod"],
    include_package_data=True,
    requires=["requests", "websocket", "pytz"]
)
