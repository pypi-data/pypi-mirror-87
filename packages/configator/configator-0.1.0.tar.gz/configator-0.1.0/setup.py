#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'configator',
  version = '0.1.0',
  description = 'A simple configuration loader',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/configator',
  download_url = 'https://github.com/acegik/configator/downloads',
  keywords = ['configuration'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)
