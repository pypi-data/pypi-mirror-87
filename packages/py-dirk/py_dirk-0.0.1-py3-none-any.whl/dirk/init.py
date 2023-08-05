import click
import os

from .utils import is_executable
from .files import EnvrcFile, KubeconfigFile


@click.command()
@click.argument(
    'directory',
    type=click.Path(
        exists=True,
        file_okay=False, dir_okay=True,
        writable=True, readable=True,
        resolve_path=True
    )
)
@click.option(
    '-c', '--configfile',
    envvar='DIRK_CONFIGFILE',
    type=click.Path(exists=True)
)
@click.option(
    '-m', '--mode',
    envvar='DIRK_MODE',
    type=click.Choice(['skip', 'replace']),
    default='skip'
)
def init(directory, configfile, mode):
    click.echo('dirk: init dirk in {directory}.'.format(directory=directory))

    click.echo('dirk: check if direnv is present on PATH.')
    if is_executable('direnv'):
        click.echo('dirk: direnv is on PATH.')

        envrc = EnvrcFile(directory=directory)
        envrc.process()

        kubeconfig = KubeconfigFile(directory=directory)
        kubeconfig.process(configfile, mode)
    else:
        click.echo('dirk: cannot find direnv on PATH.')
        click.echo('dirk: please make sure that direnv has been installed.')
