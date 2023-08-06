"""

Custom 'jenkins' command, that will talk to a Jenkins instance
and set up a build job for this project.

"""

import os
import sys

import setuptools

import jenkins
import git
import jinja2


class JenkinsCommand(setuptools.Command):
    """Tell Jenkins about this project."""

    description = "Set up Jenkins job for this project"

    DEFAULT_JENKINS = "http://localhost:8002/"

    DEFAULT_TEMPLATE = "rjgtoys.xml.j2"

    user_options = [
        ('jenkins-url=', None, "Jenkins service to talk to (default: %s" % (DEFAULT_JENKINS)),
        ('jenkins-template=', None, "Template for Jenkins job (default: built-in)"),
        ('jenkins-git-remote=', None, "Local remote name of repo to build (default: origin)"),
        ('jenkins-git-branch=', None, "Branch Jenkins is to build (default: master)"),
        ('build', None, "Trigger a build now"),
    ]

    def initialize_options(self):
        """Set initial values for the command options."""
        self.jenkins_url = self.DEFAULT_JENKINS
        self.jenkins_template = os.path.join(os.path.dirname(__file__), self.DEFAULT_TEMPLATE)
        self.jenkins_git_remote = 'origin'
        self.jenkins_git_branch = 'master'
        self.build = False

    def finalize_options(self):
        """Set final values for the command options."""
        self.jenkins_template_dir, self.jenkins_template_name = os.path.split(self.jenkins_template)

    def run(self):
        """Do Jenkins setup."""

        name = self.distribution.get_name()

        service = jenkins.Jenkins(self.jenkins_url)

        job_path = name.replace('.', '/')

        if self.build:
            print("Triggering build...")
            service.build_job(job_path)
            return

        config = self._render_template(self.jenkins_template)

        try:
            info = service.get_job_info(job_path)
        except jenkins.JenkinsException:
            info = None

        if info:
            print("Reconfigure existing job...")
            service.reconfig_job(job_path, config)
        else:
            print("Create new job...")
            service.create_job(job_path, config)

    def _render_template(self, template):
        """Find and render a template."""

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(template)), autoescape=jinja2.select_autoescape(['xml'])
        )

        try:
            tpl = env.get_template(os.path.basename(template))
        except:
            print("Template %s not found" % (template))
            raise

        # TODO: work out how to list the upstreams
        upstreams = ""

        dist = self.distribution
        name = dist.get_name()

        # Figure out Git repo URL

        project_dir = os.path.dirname(sys.modules['__main__'].__file__)

        working_repo = git.Repo(project_dir)

        remote = working_repo.remotes[self.jenkins_git_remote].url
        # Hack!
        if remote.startswith('/'):
            remote = "file://" + remote

        return tpl.render(
            description=dist.get_description(),
            name=name,
            gitrepo=remote,
            gitbranch=self.jenkins_git_branch,
            upstreams=upstreams,
            python=sys.executable,
        )
