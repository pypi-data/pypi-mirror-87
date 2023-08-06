#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

__version__ = "1.5.1"
URL = "https://github.com/xeroc/python-graphenelib"

setup(
    name="graphenelib",
    version=__version__,
    description="Python library for graphene-based blockchains",
    long_description=open("README.md").read(),
    download_url="{}/tarball/{}".format(URL, __version__),
    author="Fabian Schuh",
    author_email="Fabian@chainsquad.com",
    maintainer="Fabian Schuh",
    maintainer_email="Fabian@chainsquad.com",
    url=URL,
    keywords=["graphene", "api", "rpc", "ecdsa", "secp256k1"],
    packages=[
        "grapheneapi",
        "graphenebase",
        "graphenestorage",
        "graphenecommon",
        "grapheneapi.aio",
        "graphenecommon.aio",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
    ],
    install_requires=open("requirements.txt").readlines(),
    extras_require={"speedups": ["secp256k1>=0.13.2"]},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
