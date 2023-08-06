#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: coderfly
@file: setup
@time: 2020/12/7
@email: coderflying@163.com
@desc: 
"""
from distutils.core import setup

# This is a list of files to install, and where
# (relative to the 'root' dir, where setup.py is)
# You could be more specific.
from pkgutil import walk_packages

files = ["things/*"]


def find_packages(path):
    # This method returns packages and subpackages as well.
    return [name for _, name, is_pkg in walk_packages([path]) if is_pkg]


install_requires = [
    'PyMySQL>=0.10.1',
    'Twisted>=17.9.0',
]

setup(name="self_scrapy_utils",
      version="0.1.3",
      description="scrapy utils include piplines, utils",
      author="coder-fly",
      author_email="coderflying@163.com",
      url="https://github.com/coder-fly",
      packages=list(find_packages('src')),
      package_dir={'': 'src'},
      long_description="""scrapy utils include piplines, utils""",
      install_requires=install_requires,
      python_requires='>=3.6',
      license="MIT",
      #
      # This next part it for the Cheese Shop, look a little down the page.
      # classifiers = []
      # python setup.py sdist build
      # twine upload dist/*
      )