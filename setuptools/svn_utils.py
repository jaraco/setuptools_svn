import os
import re
import sys
import codecs
from distutils import log
import xml.dom.pulldom

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

#requires python >= 2.4
from subprocess import Popen as _Popen, PIPE as _PIPE

#NOTE: Use of the command line options
#      require SVN 1.3 or newer (December 2005)
#      and SVN 1.3 hsan't been supported by the
#      developers since mid 2008.


#svnversion return values (previous implementations return max revision)
#   4123:4168     mixed revision working copy
#   4168M         modified working copy
#   4123S         switched working copy
#   4123:4168MS   mixed revision, modified, switched working copy
_SVN_VER_RE = re.compile(r'(?:([\-0-9]+):)?(\d+)([a-z]*)\s*$', re.I)


#subprocess is called several times with shell=(sys.platform=='win32')
#see the follow for more information:
#       http://bugs.python.org/issue8557
#       http://stackoverflow.com/questions/5658622/
#              python-subprocess-popen-environment-path
def _run_command(args, stdout=_PIPE, stderr=_PIPE):
        #regarding the shell argument, see: http://bugs.python.org/issue8557
        try:
            proc = _Popen(args, stdout=stdout, stderr=stderr,
                          shell=(sys.platform == 'win32'))

            data = proc.communicate()[0]
        except OSError:
            return 1, ''

        #TODO: this is probably NOT always utf-8
        try:
            data = unicode(data, encoding='utf-8')
        except NameError:
            data = str(data, encoding='utf-8')

        #communciate calls wait()
        return proc.returncode, data


def _get_entry_name(entry):
    return entry.getAttribute('path')


def _get_entry_schedule(entry):
    schedule = entry.getElementsByTagName('schedule')[0]
    return "".join([t.nodeValue
                    for t in schedule.childNodes
                    if t.nodeType == t.TEXT_NODE])


def parse_revision(path):
    code, data = _run_command(['svnversion', '-c', path])

    if code:
        log.warn("svnversion failed")
        return 0
    else:
        log.warn('Version: %s' % data.strip())

    parsed = _SVN_VER_RE.match(data)
    if parsed:
        try:
            #No max needed this command summarizes working copy since 1.0
            return int(parsed.group(2))
        except ValueError:
            #This should only happen if the revision is WAY too big.
            pass
    return 0

#TODO: Need to do this with the -R because only root has .svn in 1.7.x
def parse_dir_entries(path):
    code, data = _run_command(['svn', 'info',
                               '--depth', 'immediates', '--xml', path])

    if code:
        log.warn("svn info failed")
        return []

    data = codecs.encode(data, 'UTF-8')

    doc = xml.dom.pulldom.parseString(data)
    entries = list()
    for event, node in doc:
        if event == 'START_ELEMENT' and node.nodeName == 'entry':
            doc.expandNode(node)
            entries.append(node)

    if entries:
        return [
            _get_entry_name(element)
            for element in entries[1:]
            if _get_entry_schedule(element).lower() != 'deleted'
        ]
    else:
        return []


#--xml wasn't supported until 1.5.x need to do -R
#TODO: -R looks like directories are seperated by blank lines
#      with dir - prepened to first directory
#      what about directories with spaces?
#          put quotes around them
#      what about the URL's?
#          same
#      convert to UTF-8 and use csv
#         delimiter = space
#
#-R without --xml parses a bit funny
def parse_externals(path):
    try:
        code, lines = _run_command(['svn',
                                    'propget', 'svn:externals', path])

        if code:
            log.warn("svn propget failed")
            return []

        lines = [line for line in lines.splitlines() if line]
    except ValueError:
        lines = []

    externals = []
    for line in lines:
        line = line.split()
        if not line:
            continue

        if urlparse.urlsplit(line[-1])[0]:
            externals.append(line[0])
        else:
            externals.append(line[-1])

    return externals


def get_svn_tool_version():
    _, data = _run_command(['svn', '--version', '--quiet'])
    if data:
        return data.strip()
    else:
        return ''

if __name__ == '__main__':
    def entries_externals_finder(dirname):
        for record in parse_dir_entries(dirname):
            yield os.path.join(dirname, record)

        for name in parse_externals(dirname):
            yield os.path.join(dirname, name)

    for name in entries_externals_finder(sys.argv[1]):
        print(name)