import re
import os

from distutils.util import convert_path

from setuptools_svn import svn_utils



# TODO will need test case
class re_finder(object):
    """
    Finder that locates files based on entries in a file matched by a
    regular expression.
    """

    def __init__(self, path, pattern, postproc=lambda x: x):
        self.pattern = pattern
        self.postproc = postproc
        self.entries_path = convert_path(path)

    def _finder(self, dirname, filename):
        f = open(filename, 'rU')
        try:
            data = f.read()
        finally:
            f.close()
        for match in self.pattern.finditer(data):
            path = match.group(1)
            # postproc was formerly used when the svn finder
            # was an re_finder for calling unescape
            path = self.postproc(path)
            yield svn_utils.joinpath(dirname, path)

    def find(self, dirname=''):
        path = svn_utils.joinpath(dirname, self.entries_path)

        if not os.path.isfile(path):
            # entries file doesn't exist
            return
        for path in self._finder(dirname, path):
            if os.path.isfile(path):
                yield path
            elif os.path.isdir(path):
                for item in self.find(path):
                    yield item

    __call__ = find


def find_files(dirname=''):
    'Primary svn_cvs entry point'
    for finder in finders:
        for item in finder(dirname):
            yield item


finders = [
    re_finder('CVS/Entries', re.compile(r"^\w?/([^/]+)/", re.M)),
    svn_utils.svn_finder,
]
