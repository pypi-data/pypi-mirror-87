"""

Custom 'lint' command.

"""
import os
import sys
import subprocess
import contextlib
import operator
import itertools

from distutils.errors import DistutilsOptionError

import setuptools


from pkg_resources import normalize_path, working_set, evaluate_marker, add_activation_listener, require


class LintCommand(setuptools.Command):
    """Run pylint and produce a report."""

    description = "Perform style checks"

    user_options = [
        ('lint-rc=', None, "Path to the pylintrc file to use (default: built-in)"),
        ('lint-report=', None, "Where to write the lint report (default: ./pylint.out)"),
        ('lint-requires', None, "List of modules needed to run pylint (default: pylint)"),
    ]

    def initialize_options(self):
        """Set initial values for the command options."""
        self.lint_rc = os.path.join(os.path.dirname(__file__), 'pylintrc')
        self.lint_report = "pylint.out"
        self.lint_requires = "pylint"

    def finalize_options(self):
        """Set final values for the command options."""
        if not os.path.isfile(self.lint_rc):
            raise DistutilsOptionError("pylintrc file '%s' does not exist" % (self.lint_rc))

    def run(self):
        """Run pylint."""

        # All this fuss with paths_on... is copied from the test command

        deps = self.install_dists(self.distribution, self.lint_requires.split(","))

        paths = map(operator.attrgetter('location'), deps)
        with self.paths_on_pythonpath(paths):
            with self.project_on_sys_path():
                self.run_lint()

    def run_lint(self):
        """Run pylint and capture the report."""

        with open(self.lint_report, "w") as report:
            #            print("Lint configuration from '%s'" % (self.lint_rc))
            print("Lint: Report will be in '%s'" % (self.lint_report))

            cmd = [sys.executable, "-m", "pylint", "--rcfile=%s" % (self.lint_rc), "rjgtoys"]

            p = subprocess.Popen(cmd, stdout=report)
            s = p.wait()
            if s == 0:
                print("Lint: PASS")
            if s & 1:
                print("Lint: Fatal error(s)")
            if s & 2:
                print("Lint: Error(s) were found")
            if s & 4:
                print("Lint: Warning(s) were found")
            if s & 8:
                print("Lint: Refactoring suggested")
            if s & 16:
                print("Lint: Style error(s) were found")
            if s & 32:
                print("Lint: Configuration (pylintrc) error")
            self._print_score()

    def _print_score(self):
        """Report the lint score."""

        report = None
        try:
            with open(self.lint_report, 'r') as f:
                for line in f:
                    if line.startswith('Your code has been rated'):
                        report = line.strip()
        except IOError as e:
            report = "Could not determine code score: %s" % (e)

        print("Lint: %s" % (report))

    # The following is copied from setuptools.command.test
    # because it appears to be needed to get dependencies
    # working.

    @staticmethod
    def install_dists(dist, lint_requires):
        """
        Install the requirements indicated by self.distribution and
        return an iterable of the dists that were built.
        """
        ir_d = dist.fetch_build_eggs(lint_requires)
        tr_d = dist.fetch_build_eggs(dist.tests_require or [])
        er_d = dist.fetch_build_eggs(
            v for k, v in dist.extras_require.items() if k.startswith(':') and evaluate_marker(k[1:])
        )
        return itertools.chain(ir_d, tr_d, er_d)

    @contextlib.contextmanager
    def project_on_sys_path(self, include_dists=None):
        """Put this project on `sys.path`."""

        # pylint: disable=unused-argument
        include_dists = include_dists or []

        # Without 2to3 inplace works fine:
        self.run_command('egg_info')

        # Build extensions in-place
        self.reinitialize_command('build_ext', inplace=1)
        self.run_command('build_ext')

        ei_cmd = self.get_finalized_command("egg_info")

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        try:
            project_path = normalize_path(ei_cmd.egg_base)
            sys.path.insert(0, project_path)
            working_set.__init__()
            # pylint: disable=not-callable
            # add_activation_listener is callable, but pylint thinks not
            add_activation_listener(lambda dist: dist.activate())
            require('%s==%s' % (ei_cmd.egg_name, ei_cmd.egg_version))
            with self.paths_on_pythonpath([project_path]):
                yield
        finally:
            sys.path[:] = old_path
            sys.modules.clear()
            sys.modules.update(old_modules)
            working_set.__init__()

    @staticmethod
    @contextlib.contextmanager
    def paths_on_pythonpath(paths):
        """
        Add the indicated paths to the head of the PYTHONPATH environment
        variable so that subprocesses will also see the packages at
        these paths.

        Do this in a context that restores the value on exit.
        """
        nothing = object()
        orig_pythonpath = os.environ.get('PYTHONPATH', nothing)
        current_pythonpath = os.environ.get('PYTHONPATH', '')
        try:
            prefix = os.pathsep.join(paths)
            to_join = filter(None, [prefix, current_pythonpath])
            new_path = os.pathsep.join(to_join)
            if new_path:
                os.environ['PYTHONPATH'] = new_path
            yield
        finally:
            if orig_pythonpath is nothing:
                os.environ.pop('PYTHONPATH', None)
            else:
                os.environ['PYTHONPATH'] = orig_pythonpath
