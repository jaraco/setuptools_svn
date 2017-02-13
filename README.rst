.. image:: https://img.shields.io/pypi/v/skeleton.svg
   :target: https://pypi.org/project/skeleton

.. image:: https://img.shields.io/pypi/pyversions/skeleton.svg

.. image:: https://img.shields.io/pypi/dm/skeleton.svg

.. image:: https://img.shields.io/travis/jaraco/skeleton/master.svg
   :target: http://travis-ci.org/jaraco/skeleton

Subversion support for Setuptools

``setuptools_svn`` implements the file finder hook for Setuptools according to
the `Setuptools documentation
<http://setuptools.readthedocs.org/en/latest/setuptools.html#adding-support-for-other-revision-control-systems>`_.

This package is for use by package authors when distributing their
Subversion-hosted project.

License
=======

License is indicated in the project metadata (typically one or more
of the Trove classifiers). For more details, see `this explanation
<https://github.com/jaraco/skeleton/issues/1>`_.

Usage
=====

Add the following to your setup.py invocation of ``setuptools.setup()``::

    setup(
        ...
        setup_requires=['setuptools_svn'],
    )
