import pathlib
from setuptools import setup

import litecoin_requests

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="litecoin-requests",
    version=litecoin_requests.__version__,
    description="Simplest Litecoin Core RPC interface.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/blockchainOSINT/litecoin-requests",
    author="fiatjaf",
    author_email="fiatjaf@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["litecoin_requests"],
    include_package_data=True,
    install_requires=["requests"],
)
