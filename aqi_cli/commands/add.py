"""
Add command for the CLI.
"""

import click
from aqi_cli.utils import make_request, get_stations, show_menu, add_to_config_file


@click.command()
@click.argument("location")
def add(location: str):
    """
    Add location to the config file.

    @TODO
    Before adding to the file:
    1. make sure the directory and the file to create is there.
    2. make sure teh entry is valid and let user select which location s/he wants to set.
    3. create a --all flag to set all the location presented in the result.
    """
    data = make_request(location)

    stations_data = get_stations(data)
    stations = [data.station for data in stations_data]
    selected_station = show_menu(stations) if len(stations) > 1 else stations[0]

    # Get uid for selected station.
    station_uid = [
        data.uid for data in stations_data if data.station == selected_station
    ]

    add_to_config_file(
        station_uid=station_uid, location=location, station=selected_station
    )
