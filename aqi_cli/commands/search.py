"""
Search command for the CLI.
"""
import click
from aqi_cli.utils import create_table_payload, make_request, get_aqi_data, show_table


@click.command()
@click.argument("query")
def search(query: str):
    """
    Search query for the city or nation to get aqi.
    """
    # Make search request to the API.
    data = make_request(query)

    # Get aqi value and station name from the response payload.
    api_data = get_aqi_data(data, query)

    # Create an info payload that resonates to the aqi values extracted.
    air_info = create_table_payload(api_data)

    # Show table with air quality information.
    show_table(air_info)
