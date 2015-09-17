# -*- coding: utf-8 -*-
from datetime import datetime
from plumbum import cli, local, ProcessExecutionError
from plumbum.commands.modifiers import FG


ansible = NotImplemented


class App(cli.Application):

    inventory = cli.SwitchAttr(
        ['--inventory', '-i'],
        cli.ExistingFile,
        default='ansible/hosts',
        help='Path to ansible inventory file',
    )

    def main(self, *args):
        global ansible
        ansible = local['ansible-playbook']['-i'][self.inventory]
        return super(App, self).main(*args)


@App.subcommand('list')
class List(cli.Application):
    DESCRIPTION = 'Lists currently installed and running versions'

    def main(self, *args):
        raise NotImplementedError


@App.subcommand('build')
class Build(cli.Application):
    DESCRIPTION = 'Build a docker image containing ready-to-use application'

    def main(self, version=None):
        if not version:
            version = generate_version_timestamp()
        build(version)


@App.subcommand('install')
class Install(cli.Application):
    DESCRIPTION = 'Installs docker image on app servers, runs containers ' \
                  'and prepares nginx configs so that application version ' \
                  'is accessible from the web'

    def main(self, version):
        install(version)


@App.subcommand('buildinst')
class BuildAndInstall(cli.Application):
    DESCRIPTION = 'Builds, then installs'

    def main(self):
        version = generate_version_timestamp()
        build(version)
        install(version)


def build(version):
    run_or_exit(ansible[
        '--connection', 'local',
        '--extra-vars', 'version=%s' % version,
        'ansible/build_version.yml',
    ])


def install(version):
    run_or_exit(ansible[
        '--extra-vars', 'version=%s' % version,
        'ansible/install_version.yml',
    ])


def run_or_exit(cmd):
    try:
        cmd & FG
    except ProcessExecutionError:
        raise SystemExit


def generate_version_timestamp():
    return datetime.now().strftime('%Y.%m.%d.%H.%M')


def main():
    App.run()
