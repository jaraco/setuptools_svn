Subversion Support for Setuptools
=================================

``setuptools_svn`` implements the file finder hook for Setuptools according to
the `Setuptools documentation
<http://setuptools.readthedocs.org/en/latest/setuptools.html#adding-support-for-other-revision-control-systems>`_.

This package is for use by package authors when distributing their
Subversion-hosted project.

Usage
-----

Add the following to your setup.py invocation of ``setuptools.setup()``::

    setup(
        ...
        setup_requires=['setuptools_svn'],
    )
