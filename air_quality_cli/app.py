"""
Entrypoint for CLI.
"""
import click

from air_quality_cli.commands import add, search, init, show


@click.group()
def cli():
    pass


cli.add_command(add)
cli.add_command(init)
cli.add_command(show)
cli.add_command(search)
