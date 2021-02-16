"""
Remove command for the CLI
"""
import json
import click

from air_quality_cli.utils import (
    make_request,
    get_stations,
    show_menu,
    remove_from_config_file,
)

from air_quality_cli.constants import (
    CONFIG_FILE,
)


@click.command()
@click.argument("location")
def remove(location: str):
    """
    Remove saved stations from a location
    """

    # Make search request to the API
    data = make_request(location)

    # Get the name of the stations and their uids
    stations_data = get_stations(data)

    # Boolean to find out whether location is saved.
    is_saved: bool = False

    # Show only the stations present in config file for the remove list
    with open(CONFIG_FILE, "r") as file:
        data = file.readline()

        data_dict = json.loads(data)

        if location in data_dict:
            is_saved = True

    # If the location is found, show the list of stations to be removed.
    if is_saved:

        stations = [
            item.station
            for item in stations_data
            if item.uid in data_dict[location]
        ]

        # Allow the user to select the station to be removed from the config file.
        selected_station = (
            show_menu(stations) if len(stations) > 1 else stations[0]
        )

        # Get uid for selected station.
        station_uid = [
            data.uid
            for data in stations_data
            if data.station == selected_station
        ]

        # Remove the selected item from the config file
        remove_from_config_file(
            station_uid=station_uid,
            location=location,
            station=selected_station,
        )

    else:
        # Simply exit with a message if no location found.
        click.echo(f"No station from {location} found.")
