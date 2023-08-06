import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="werf_chart_repo_doit_tasks",
    version="1.0.4",
    url="https://github.com/ilya-lesikov/werf_chart_repo_doit_tasks",
    license="MIT",

    author="Ilya Lesikov",
    author_email="ilya@lesikov.com",

    description="Doit Tasks for managing Werf chart repo",
    long_description=read("README.rst"),

    packages=find_packages(exclude=("tests",)),

    install_requires=[
      "doit >= 0.33.1, < 0.34",
    ],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
