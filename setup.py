#!/usr/bin/env python
# Generated by jaraco.develop (https://bitbucket.org/jaraco/jaraco.develop)
import io

import setuptools

with io.open('README.txt', encoding='utf-8') as readme:
	long_description = readme.read()
with io.open('CHANGES.txt', encoding='utf-8') as changes:
	long_description += '\n\n' + changes.read()

setup_params = dict(
	name='setuptools_svn',
	use_hg_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description="setuptools_svn",
	long_description=long_description,
	url="https://bitbucket.org/jaraco/setuptools_svn",
	packages=setuptools.find_packages(),
	setup_requires=[
		'hgtools',
		'pytest-runner',
	],
	tests_require=[
		'pytest',
	],
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
	],
	entry_points={
        "setuptools.file_finders":
            ["svn_cvs = setuptools_svn:find_files"],
	},
)
if __name__ == '__main__':
	setuptools.setup(**setup_params)
