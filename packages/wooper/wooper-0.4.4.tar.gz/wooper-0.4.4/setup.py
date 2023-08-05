#!/usr/bin/env python

from codecs import open as _open
from os import path

from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))

with _open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with _open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    REQUREMENTS = f.read().splitlines()

setup(
    name='wooper',
    version="0.4.4",
    description="FrisbyJS-inspired REST API testing helpers and steps "
        "for 'behave' behavior-driven development testing library",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Yauhen Kirylau',
    author_email='actionless.loveless@gmail.com',
    url='http://github.com/actionless/wooper',
    license='GPL3',
    platforms=["any"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUREMENTS,
    classifiers=[
        # @TODO: change status
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        # @TODO: add testers
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
