"""
Search command for the CLI.
"""
import click

from typing import List, Tuple

from air_quality_cli.utils import (
    create_table_payload,
    make_request,
    get_aqi_data,
    show_table,
    show_menu,
    get_stations,
)


@click.command()
@click.argument("query")
@click.option("--select", is_flag=True)
def search(select, query: str):
    """
    Search query for the city or nation to get aqi.
    """

    # Make search request to the API.
    data = make_request(query)

    # Get aqi value and station name from the response payload.
    api_data = get_aqi_data(data, query)

    # Show only one station's data if called with --select flag
    if select:
        click.echo("Asked with search")

        # Using simple-term-menu to show the list of stations
        # Get the name of stations and their uid from the response data.
        stations_data = get_stations(data)

        # Filter out just the stations.
        stations = [data.station for data in stations_data]

        # Allow user to select station to add to the config file.
        selected_station = (
            show_menu(stations) if len(stations) > 1 else stations[0]
        )

        # Declare a list of tuple to hold the tuple of single station.
        single_station_list: List[Tuple[str, str]] = []

        for item in api_data:
            if item[0] == selected_station:
                single_station_list.append(item)

        air_info = create_table_payload(single_station_list)

    else:
        # Create an info payload that resonates to the aqi values extracted.
        air_info = create_table_payload(api_data)

    # Show table with air quality information.
    show_table(air_info)
