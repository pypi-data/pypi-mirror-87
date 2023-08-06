"""

Custom 'test' command.

"""

import sys
import os
import stat

# See: http://pytest.org/latest/goodpractises.html

import setuptools
from setuptools.command.test import test as TestCommand


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def readfile(fname):
    """Read a file and return its content."""
    return open(os.path.join(os.path.dirname(sys.modules['__main__'].__file__), fname)).read()


def find_all_directories(sources):
    """Start with a list of directories, find all subdirectories."""

    r = set()
    for s in sources:
        r.update(_find_all_dirs(s))

    return r


def _find_all_dirs(root):
    """Find all directories under root (which might not be a directory)."""

    q = [root]
    while q:
        here = q.pop()
        # Hack: omit anything that looks like it might involve templating...
        if '{' in here or '}' in here:
            continue
        s = os.lstat(here)
        if not stat.S_ISDIR(s.st_mode):
            continue
        yield here

        subs = os.listdir(here)

        q.extend(os.path.join(here, s) for s in subs)


class PyTest(TestCommand):
    """An extended test command that produces coverage reports of tests."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['-s', 'tests']  # preserve stdout
        self.test_suite = True

    def run_tests(self):
        # pylint: disable=too-many-locals
        # pylint: disable=import-outside-toplevel
        # import here, because outside, the eggs aren't loaded

        import pytest
        import coverage
        import time
        import re

        # Note that here, __main__ refers to the calling project's
        # "setup.py"

        project_root = os.path.dirname(sys.modules['__main__'].__file__)

        cov_file = os.path.join(project_root, '.coverage')
        if os.path.exists(cov_file):
            os.unlink(cov_file)

        packages = setuptools.find_packages(where=project_root)

        sources = [p.replace('.', '/') for p in packages]
        fixtures = os.path.join(project_root, 'tests/fixtures')
        if os.path.isdir(fixtures):
            sources.append(fixtures)

        # Include all subdirectories, so coverage tells us if we've
        # completely missed a module or two

        sources = find_all_directories(sources)

        cov = coverage.coverage(source=sources)

        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.save()

        cov_dir = os.path.join(project_root, 'htmlcov')
        try:
            cov.html_report(directory=cov_dir)
        except coverage.misc.CoverageException as e:
            print("Coverage report error: %s" % (e))

        index_html = os.path.join(cov_dir, 'index.html')

        if os.path.isfile(index_html):

            # Now fix up the report to have a nice title

            cov_title = "Coverage report for %s created at %s" % (
                ",".join(packages),
                time.strftime("%Y-%m-%d %H:%M:%S"),
            )

            report = readfile(index_html)
            report = re.sub('Coverage report', cov_title, report)

            with open(index_html, "w") as f:
                f.write(report)

        sys.exit(errno)
