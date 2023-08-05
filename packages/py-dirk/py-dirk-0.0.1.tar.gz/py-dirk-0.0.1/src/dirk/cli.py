import click

from .init import init


@click.group()
def main():
    pass


main.add_command(init)
