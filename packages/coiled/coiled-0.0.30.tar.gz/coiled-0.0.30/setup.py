#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

import versioneer

setup(
    name="coiled",
    url="https://coiled.io",
    maintainer="Coiled",
    maintainer_email="info@coiled.io",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="",
    packages=find_packages(),
    include_package_data=True,
    long_description=(open("README.md").read() if exists("README.md") else ""),
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=list(open("requirements.txt").read().strip().split("\n")),
    entry_points={"console_scripts": ["coiled=coiled.cli.core:cli"]},
    python_requires=">=3.6",
)
