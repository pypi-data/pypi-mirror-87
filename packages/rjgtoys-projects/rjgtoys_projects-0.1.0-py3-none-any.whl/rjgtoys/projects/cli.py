"""
Command line tool to help with rjgtoys projects.

Uses cookiecutter to build a new empty project tree.

"""

#!/usr/bin/python3.8
#
# Make a new rjgtoy
#
# Can accept command line options for the variables
#

import argparse
import io
import os

from cookiecutter.generate import generate_files
from cookiecutter.config import merge_configs
from cookiecutter.exceptions import (
    OutputDirExistsException
)

import poyo # use cookiecutter's YAML parser


class CommandFailed(Exception):
    """Raised to indicate command failure."""

    pass


class ToyMaker:
    """Command-line tool to create new projects."""

    TITLE = "Build a new rjgtoys project"

    DEFAULT_TEMPLATE = 'rjgtoys'

    DEFAULT_CONFIG = os.path.expanduser("~/.config/rjgtoys/projects/projects.conf")

    CONFIG_ITEMS = (
        ('project.family', 'Group that the project belongs to'),
        ('project.id', 'Name of the project, for directories etc.'),
        ('project.name', 'Name of the project, for docs'),
        ('project.title', 'One line description of the project'),
        ('author.name', 'Full name of the author'),
        ('author.email', 'Email address of author'),
        ('github.base', 'Base URL for github repos'),
        ('copyright.year', 'Year to include in copyright notices'),
    )

    def build_parser(self):
        """Build a command line parser."""

        p = argparse.ArgumentParser(
            self.TITLE,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        p.add_argument(
            "--name",
            metavar="NAME",
            help="Public name of the project, for docs etc.",
            default=argparse.SUPPRESS
        )
        p.add_argument(
            '--id',
            metavar='IDENT',
            help="Internal name of the project, for directories etc.",
            default=argparse.SUPPRESS
        )
        p.add_argument(
            "--title",
            metavar="TEXT",
            help="One-line title for the project",
            required=True,
            default=argparse.SUPPRESS
        )
        p.add_argument(
            "--template",
            metavar="PATH",
            help="Template name or path",
            default=self.DEFAULT_TEMPLATE
        )
        p.add_argument(
            "--update",
            action="store_true",
            help="Update an existing project",
            default=False
        )
        p.add_argument(
            "--config",
            metavar="PATH",
            help="Configuration to use",
            default=self.DEFAULT_CONFIG
        )
        p.add_argument(
            "--dry-run", "-n",
            action="store_true",
            help="Don't generate anything, just validate",
            default=False
        )

        return p

    def main(self, argv=None):
        """Main program entry point."""

        p = self.build_parser()

        args = p.parse_args(argv)

        try:
            return self.run(args) or 0
        except CommandFailed as e:
            print(str(e))
            return 1

    def run(self, args):
        """Do the work."""

        # Config must exist and be valid

        defaults = self.get_config(args.config)

        template_path = os.path.join(os.path.dirname(__file__), 'templates', args.template)

        project_name = getattr(args, 'name', None)
        project_id = getattr(args, 'id', None)

        if (project_name, project_id) == (None, None):
            self.fail("At least one of --name or --id must be given.")

        if project_name is None:
            project_name = project_id.title()
        elif project_id is None:
            project_id = project_name.lower()

        project_dir = project_name

        if os.path.exists(project_dir):
            if not args.update:
                self.fail(f"Project directory {project_dir} exists; use --update if you want to update it")
            print(f"Updating {project_dir}")

        context = dict(
            project=dict(
                id=project_id,
                name=project_name,
                title=args.title,
            )
        )

        context = merge_configs(defaults, context)

        # cookiecutter requires a 'cookiecutter' namespace
        # so make everything available there too.

        context['cookiecutter'] = context

        # Validate and dump the config

        w = max(len(path) for (path, _) in self.CONFIG_ITEMS)
        w += 3

        ok = True
        for (path, desc) in self.CONFIG_ITEMS:
            try:
                v = getpath(context, path)
            except KeyError:
                ok = False
                v = f"MISSING: {desc}"

            print("%s %s" % (path.ljust(w, '.'), v))

        if args.dry_run:
            print("Dryrun: nothing changed or created")
            return []

        if not ok:
            self.fail("Configuration errors must be fixed first")

        try:
            result = self.generate(
                repo_dir=template_path,
                context=context,
                update=args.update
            )
        except OutputDirExistsException as e:
            print(e)
            self.fail("Use --update if you want to replace files")

        # TODO: Verify, report?

        return result

    @staticmethod
    def fail(msg):
        """This command has failed."""

        # Not sure if simply raising the exception is clearer.
        raise CommandFailed(msg)

    @staticmethod
    def generate(repo_dir, context, update):
        """Create project from local context and project template."""

        result = generate_files(
            repo_dir=repo_dir,
            context=context,
            overwrite_if_exists=update,
            skip_if_file_exists=not update,
            output_dir='.',
        )
        return result

    def get_config(self, config_path):
        """Retrieve the config from the specified path, returning a config dict."""
        # Cut-down version of the function in cookiecutter.config

        if not os.path.exists(config_path):
            self.fail(
                f"Config file {config_path} does not exist."
            )

        with io.open(config_path, encoding='utf-8') as file_handle:
            try:
                yaml_dict = poyo.parse_string(file_handle.read())
            except poyo.exceptions.PoyoException as e:
                self.fail(
                    f"Unable to parse config file {config_path}: {e}"
                )

        return yaml_dict

def getpath(data, path):
    """Traverse nested dictionaries with a 'dotted path'.

    x['a.b'] == x['a']['b']

    """

    for p in path.split('.'):
        data = data[p]

    return data

def main():
    """Script entry point; processes the command line and exits."""

    # pylint: disable=import-outside-toplevel

    import sys
    cmd = ToyMaker()
    sys.exit(cmd.main())


if __name__ == "__main__":
    main()
