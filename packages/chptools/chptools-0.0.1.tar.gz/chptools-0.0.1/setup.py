from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
		name="chptools",
		version="0.0.1",
		author="Biorad",
		author_email="cyz_19930904@163.com",
		description="A series of Chinese processing tools",
		long_description=open("README.rst").read(),
		license="MIT",
		url="https://github.com/cyzLoveDream/CPTools",
		packages=['cptools'],
		install_requires=[
			"pyahocorasick",
			]
		)
