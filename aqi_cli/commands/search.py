"""
Search command for the CLI.
"""
import click
from aqi_cli.utils import make_request, get_aqi_data


@click.command()
@click.argument("query")
def search(query: str):
    """
    Search query for the city or nation to get aqi.
    """
    data = make_request(query)
    api_data = get_aqi_data(data, query)

    # @TODO pretty print the data with tabulate.
    print(api_data)
