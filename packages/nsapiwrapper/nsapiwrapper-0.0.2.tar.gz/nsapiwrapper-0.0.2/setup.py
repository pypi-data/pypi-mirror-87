#!/usr/bin/env python
"""
Copyright (c) 2019 Joshua W
"""


version = '0.0.2'

from setuptools import setup
setup(name='nsapiwrapper',
      install_requires=["beautifulsoup4==4.8.0", "ezurl==0.1.3.25",
                        "requests==2.22.*", "xmltodict==0.12.0", "lxml==4.6.2" ],
      version=version,
      description='Simple Nationstates API Wrapper',
      author='Joshua W',
      author_email='DolphDevgithub@gmail.com',
      keywords=["nationstates"],
      packages=["nsapiwrapper"],
      classifiers=["License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6"]
                    )
