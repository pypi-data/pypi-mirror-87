import os
import fileinput
import shutil
import click

from .settings import EXPORT_KUBECONFIG, ENVRC_FILENAME, KUBECONFIG_FILENAME


class EnvrcFile:
    def __init__(self, directory):
        self.path = os.path.join(directory, ENVRC_FILENAME)

    def exists(self):
        return os.path.isfile(self.path)

    def create(self):
        with open(self.path, 'w') as file:
            file.write('{export}\n'.format(export=EXPORT_KUBECONFIG))

    def __append_export(self):
        with open(self.path, 'a') as file:
            file.write('\n{export}\n'.format(export=EXPORT_KUBECONFIG))

    def __replace_export(self):
        modified = False
        with fileinput.input(files=(self.path,), inplace=True) as file:
            for line in file:
                if line.strip().startswith('export KUBECONFIG='):
                    print(EXPORT_KUBECONFIG, end='')
                    modified = True
                else:
                    print(line, end='')
        return modified

    def replace_or_append_export(self):
        modified = self.__replace_export()
        if not modified:
            self.__append_export()

    def allow(self):
        os.system('direnv allow {path}'.format(path=self.path))

    def process(self):
        if self.exists():
            click.echo('dirk: {path} does already exist.'.format(path=self.path))
            click.echo('dirk: process {path}.'.format(path=self.path))
            self.replace_or_append_export()
        else:
            click.echo('dirk: {path} does not exist.'.format(path=self.path))
            click.echo('dirk: create {path}.'.format(path=self.path))
            self.create()
        click.echo('dirk: direnv allow {path}.'.format(path=self.path))
        self.allow()


class KubeconfigFile:
    def __init__(self, directory):
        self.path = os.path.join(directory, KUBECONFIG_FILENAME)

    def exists(self):
        return os.path.isfile(self.path)

    def create(self):
        open(self.path, 'a').close()

    def replace(self, configfile):
        shutil.copyfile(configfile, self.path)

    def set_mode(self):
        os.chmod(self.path, 0o600)

    def process(self, configfile, mode):
        if self.exists():
            click.echo('dirk: {path} does already exist'.format(path=self.path))
            if configfile:
                if mode == 'skip':
                    click.echo('dirk: skip writing {file} to existing kubeconfig.'.format(file=configfile))
                if mode == 'replace':
                    click.echo('dirk: replace existing kubeconfig by {file}.'.format(file=configfile))
                    self.replace(configfile)
        else:
            click.echo('dirk: {path} does not exist.'.format(path=self.path))
            if configfile:
                click.echo('dirk: write {file} to kubeconfig.'.format(file=configfile))
                self.replace(configfile)
            else:
                click.echo('dirk: create empty {path}.'.format(path=self.path))
                self.create()
            self.set_mode()
