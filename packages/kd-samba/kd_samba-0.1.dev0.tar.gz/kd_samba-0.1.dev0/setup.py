#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, setuptools,find_packages

def readme():
	with open('README.rst') as f:
		return f.read()

package_data = {'kd_reports': ['LICENSE.txt']}
packages=find_packages()

setup(
	name="kd_samba",
	version="0.1DEV",
	description="Web interface for managing samba users",
	long_description=readme(),
	author = "Federico Campoli",
	author_email = "thedoctor@pgdba.org",
	maintainer = "Federico Campoli", 
	maintainer_email = "thedoctor@pgdba.org",
	url="https://gitlab.com/kamedata/py_samba_gui",
	license="BSD License",
	platforms=[
		"linux"
	],
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"Intended Audience :: Information Technology",
		"Intended Audience :: System Administrators",
		"Natural Language :: English",
		"Operating System :: POSIX :: BSD",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Topic :: Database :: Database Engines/Servers",
		"Topic :: Other/Nonlisted Topic"
	],
	py_modules=[
		"kd_samba.__init__",
	],
	install_requires=[
		'fastapi',
        'pydantic',
        'uvicorn'
	],
	include_package_data = True, 
	package_data=package_data,
	packages=packages,
	python_requires='>=3.7',
	keywords='samba',
	
)
