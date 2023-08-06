# NOTE TO MYSELF: DON'T FUCKING IMPORT ANY MODULE FROM MY PACKAGE HERE !
import setuptools


with open("README.md", "r") as file:
    LONG_DESCRIPTION = file.read()


NAME = "pyrustic"
VERSION = "0.0.2"
AUTHOR = "Pyrustic Evangelist"
EMAIL = "pyrustic@protonmail.com"
DESCRIPTION = "Lightweight software suite to help develop, package, and publish Python desktop applications"
URL = "https://github.com/pyrustic/pyrustic"


setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
