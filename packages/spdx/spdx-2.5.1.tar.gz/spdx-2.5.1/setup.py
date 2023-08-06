from setuptools import setup, find_packages

with open('README.rst') as f:
    desc = f.read()

setup(
    name = "spdx",
    version = "2.5.1",
    packages = ['spdx'],
    package_data = {'spdx': ['data/*.txt', 'data/db.json']},
    author = "Brendan Molloy",
    author_email = "brendan+pypi@bbqsrc.net",
    description = "SPDX license list database",
    license = "CC0-1.0",
    keywords = ["spdx", "licenses", "database"],
    url = "https://github.com/bbqsrc/spdx-python",
    long_description=desc,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
