#!/usr/bin/python3

try:
    from rjgtoys.projects import setup
except ImportError:
    from setuptools import setup

setup(
    name = "rjgtoys-{{project.name}}",
    version = "0.0.1",
    author = "Robert J Gautier",
    author_email = "bob.gautier@gmail.com",
    url = "https://github.com/bobgautier/rjgtoys-{{project.name}}",
    description = ("{{project.title}}"),
    namespace_packages=['rjgtoys'],
    packages = ['rjgtoys','rjgtoys.{{project.name}}'],
    install_requires = [
    ],
    extras_require = {
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
