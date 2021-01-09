"""
CLI initialization command.
"""
import click
from rich.prompt import Prompt

from aqi_cli import console
from aqi_cli.utils import add_credential
from aqi_cli.constants import TOKEN_HELP_MSG


@click.command()
def init():
    """
    Initialize the CLI by prompting user to enter API token.
    """
    console.print(TOKEN_HELP_MSG)
    token = Prompt.get_input(
        console, ":key: Enter your API Token (hidden) ", password=True
    )

    add_credential(token)
