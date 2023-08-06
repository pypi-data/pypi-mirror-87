#!/usr/bin/env python3

# Note!
# ' are required, do not use any ".

# setup.
from setuptools import setup, find_packages
setup(
	name='r3stapi',
	version='0.6.3',
	description='Some description.',
	url="http://github.com/vandenberghinc/r3stapi",
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		"fil3s",
		"r3sponse",
		"fir3base",
	])