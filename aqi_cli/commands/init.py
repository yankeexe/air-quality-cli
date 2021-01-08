"""
CLI initialization command.
"""
import click
from rich.prompt import Prompt

from aqi_cli import console
from aqi_cli.utils import add_credential


@click.command()
def init():
    """
    Initialize the CLI by prompting user to enter API token.
    """
    console.print("Get your token here: https://aqicn.org/data-platform/token/#/\n")
    # token: str = click.prompt("Enter your API Token (hidden)", hide_input=True)
    token = Prompt.get_input(
        console, ":key: Enter your API Token (hidden) ", password=True
    )

    add_credential(token)
