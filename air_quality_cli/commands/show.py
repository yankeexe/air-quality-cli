"""
Show command for the CLI.
"""
import click

from air_quality_cli.utils import (
    concurrent_requests,
    filter_show_stations,
    get_config_stations,
    show_table,
    create_table_payload,
)


@click.command()
def show():
    """
    Shows all the stations store in stations config dictionary.

    stations config: ~/.aqi/stations
    """
    config_data = get_config_stations()

    aqi_data = concurrent_requests(config_data)
    filtered = filter_show_stations(aqi_data, config_data)

    # Create an info payload that resonates to the aqi values filtered.
    air_info = create_table_payload(filtered)

    # Show table with air quality information.
    show_table(air_info)
