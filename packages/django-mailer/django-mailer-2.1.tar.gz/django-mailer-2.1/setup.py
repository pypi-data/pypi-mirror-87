#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="django-mailer",
    version="2.1",
    description="A reusable Django app for queuing the sending of email",
    long_description=open("docs/usage.rst").read() + open("CHANGES.rst").read(),
    author="Pinax Team",
    author_email="developers@pinaxproject.com",
    url="http://github.com/pinax/django-mailer/",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={'mailer': ['locale/*/LC_MESSAGES/*.*']},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
    ],
    install_requires=[
        'Django >= 1.11',
        'lockfile >= 0.8',
        'six',
        ],
)
