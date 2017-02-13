import os
import re

from tests import environment
from tests.test_svn import needs_svn
import setuptools_svn
from setuptools_svn import svn_utils

class TestDummyOutput(environment.ZippedEnvironment):

    def setUp(self):
        self.datafile = os.path.join('tests',
                                     'data', "dummy.zip")
        self.dataname = "dummy"
        super(TestDummyOutput, self).setUp()

    def _run(self):
        code, data = environment.run_setup_py(["sdist"],
                                              pypath=self.old_cwd,
                                              data_stream=0)
        if code:
            info = "DIR: " + os.path.abspath('.')
            info += "\n  SDIST RETURNED: %i\n\n" % code
            info += data
            raise AssertionError(info)

        datalines = data.splitlines()

        possible = (
            "running sdist",
            "running egg_info",
            "creating dummy\.egg-info",
            "writing dummy\.egg-info",
            "writing top-level names to dummy\.egg-info",
            "writing dependency_links to dummy\.egg-info",
            "writing manifest file 'dummy\.egg-info",
            "reading manifest file 'dummy\.egg-info",
            "reading manifest template 'MANIFEST\.in'",
            "writing manifest file 'dummy\.egg-info",
            "creating dummy-0.1.1",
            "making hard links in dummy-0\.1\.1",
            "copying files to dummy-0\.1\.1",
            "copying \S+ -> dummy-0\.1\.1",
            "copying dummy",
            "copying dummy\.egg-info",
            "hard linking \S+ -> dummy-0\.1\.1",
            "hard linking dummy",
            "hard linking dummy\.egg-info",
            "Writing dummy-0\.1\.1",
            "creating dist",
            "creating 'dist",
            "Creating tar archive",
            "running check",
            "adding 'dummy-0\.1\.1",
            "tar .+ dist/dummy-0\.1\.1\.tar dummy-0\.1\.1",
            "gzip .+ dist/dummy-0\.1\.1\.tar",
            "removing 'dummy-0\.1\.1' \\(and everything under it\\)",
        )

        print("    DIR: " + os.path.abspath('.'))
        for line in datalines:
            found = False
            for pattern in possible:
                if re.match(pattern, line):
                    print("   READ: " + line)
                    found = True
                    break
            if not found:
                raise AssertionError("Unexpexected: %s\n-in-\n%s"
                                     % (line, data))

        return data

    def test_sources(self):
        self._run()


class TestSvn(environment.ZippedEnvironment):

    def setUp(self):
        version = svn_utils.SvnInfo.get_svn_version()
        if not version:  # None or Empty
            return

        self.base_version = tuple([int(x) for x in version.split('.')][:2])

        if not self.base_version:
            raise ValueError('No SVN tools installed')
        elif self.base_version < (1, 3):
            raise ValueError('Insufficient SVN Version %s' % version)
        elif self.base_version >= (1, 9):
            # trying the latest version
            self.base_version = (1, 8)

        self.dataname = "svn%i%i_example" % self.base_version
        self.datafile = os.path.join('tests',
                                     'data', self.dataname + ".zip")
        super(TestSvn, self).setUp()

    @needs_svn
    def test_walksvn(self):
        if self.base_version >= (1, 6):
            folder2 = 'third party2'
            folder3 = 'third party3'
        else:
            folder2 = 'third_party2'
            folder3 = 'third_party3'

        # TODO is this right
        expected = set([
            os.path.join('a file'),
            os.path.join(folder2, 'Changes.txt'),
            os.path.join(folder2, 'MD5SUMS'),
            os.path.join(folder2, 'README.txt'),
            os.path.join(folder3, 'Changes.txt'),
            os.path.join(folder3, 'MD5SUMS'),
            os.path.join(folder3, 'README.txt'),
            os.path.join(folder3, 'TODO.txt'),
            os.path.join(folder3, 'fin'),
            os.path.join('third_party', 'README.txt'),
            os.path.join('folder', folder2, 'Changes.txt'),
            os.path.join('folder', folder2, 'MD5SUMS'),
            os.path.join('folder', folder2, 'WatashiNiYomimasu.txt'),
            os.path.join('folder', folder3, 'Changes.txt'),
            os.path.join('folder', folder3, 'fin'),
            os.path.join('folder', folder3, 'MD5SUMS'),
            os.path.join('folder', folder3, 'oops'),
            os.path.join('folder', folder3, 'WatashiNiYomimasu.txt'),
            os.path.join('folder', folder3, 'ZuMachen.txt'),
            os.path.join('folder', 'third_party', 'WatashiNiYomimasu.txt'),
            os.path.join('folder', 'lalala.txt'),
            os.path.join('folder', 'quest.txt'),
            # The example will have a deleted file
            #  (or should) but shouldn't return it
        ])
        self.assertEqual(set(x for x in setuptools_svn.find_files()), expected)

