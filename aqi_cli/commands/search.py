"""
Search command for the CLI.
"""
import click
from rich import table
from aqi_cli.utils import create_table_payload, make_request, get_aqi_data, show_table


@click.command()
@click.argument("query")
def search(query: str):
    """
    Search query for the city or nation to get aqi.
    """
    data = make_request(query)
    api_data = get_aqi_data(data, query)

    # @TODO pretty print the data with tabulate.
    table_info = create_table_payload(api_data)
    show_table(table_info)
