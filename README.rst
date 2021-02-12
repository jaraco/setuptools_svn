.. image:: https://img.shields.io/pypi/v/setuptools_svn.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/setuptools_svn.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/setuptools_svn

.. image:: https://github.com/jaraco/setuptools_svn/workflows/tests/badge.svg
   :target: https://github.com/jaraco/setuptools_svn/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

Subversion support for Setuptools

``setuptools_svn`` implements the file finder hook for Setuptools according to
the `Setuptools documentation
<http://setuptools.readthedocs.org/en/latest/setuptools.html#adding-support-for-other-revision-control-systems>`_.

This package is for use by package authors when distributing their
Subversion-hosted project.

Usage
=====

Add the following to your setup.py invocation of ``setuptools.setup()``::

    setup(
        ...
        setup_requires=['setuptools_svn'],
    )
