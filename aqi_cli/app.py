"""
Entrypoint for CLI.
"""
import click

from aqi_cli.commands import add, search, init


@click.group()
def cli():
    pass


cli.add_command(add)
cli.add_command(init)
cli.add_command(search)
