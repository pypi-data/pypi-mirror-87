#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import setup, find_packages, Command

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup_requirements = ["pytest-runner",]
test_requirements = ["pytest"]

packages = [package for package in find_packages() if package.startswith("api")]

# Determine which namespaces are needed.
namespaces = ["api"]


setup(
    author="vikas",
    author_email="x.vikassoni@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="api-validation package.",
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="api",
    name="ApiValidations",
    packages=packages,
    namespace_packages=namespaces,
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/soni-vikas/easy-api-validation",
    version="1.0.0",
    zip_safe=False,
    package_dir={"": "."},
    cmdclass={},
)
