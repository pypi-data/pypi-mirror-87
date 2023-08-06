#!/usr/bin/env python3

# Note!
# ' are required, do not use any ".

# setup.
from setuptools import setup, find_packages
setup(
	name='fir3base',
	version='0.6.3',
	description='Some description.',
	url="http://github.com/vandenberghinc/fir3base",
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	zip_safe=False,
	install_requires=[
		"firebase-admin",
		"django",
	],)