#! /usr/bin/env python

from setuptools import setup

setup(
    name="warc3-wet-clueweb09",
    version="0.2.4",
    description="Python library to work with ARC and WARC files, with fixes for ClueWeb09",
    long_description=open('Readme.rst').read(),
    license='GPLv2',
    author="Anand Chitipothu, Noufal Ibrahim, Ryan Chartier, Jan Pieter Bruins Slot, Almer S. Tigelaar, Willian Zhang",
    author_email="info@archive.org",
    url="https://github.com/seanmacavaney/warc3-clueweb",
    packages=["warc3_wet_clueweb09"],
    platforms=["any"],
    package_data={'': ["LICENSE", "Readme.rst"]},
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
