#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'configator',
  version = '0.1.4',
  description = 'A simple CONFIGuration propagATOR',
  author = 'skelethon',
  license = 'GPL-3.0',
  url = 'https://github.com/skelethon/configator',
  download_url = 'https://github.com/skelethon/configator/downloads',
  keywords = ['configuration', "redis", "pub/sub"],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)
