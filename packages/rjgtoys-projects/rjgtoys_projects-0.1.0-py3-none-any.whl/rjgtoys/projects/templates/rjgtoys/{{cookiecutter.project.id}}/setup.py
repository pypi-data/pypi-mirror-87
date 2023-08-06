#!/usr/bin/python3

try:
    from rjgtoys.projects import setup
except ImportError:
    from setuptools import setup

setup(
    name="rjgtoys-{{project.id}}",
    version="0.0.1",
    author="{{author.name}}",
    author_email="{{author.email}}",
    url="{{github.base}}{{project.family}}-{{project.name}}",
    description=("{{project.title}}"),
    namespace_packages=['{{project.family}}'],
    packages=['{{project.family}}', '{{project.family}}.{{project.id}}'],
    install_requires=[],
    extras_require={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
