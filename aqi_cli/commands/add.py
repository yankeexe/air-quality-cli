"""
Add command for the CLI.
"""
import click
from aqi_cli.utils import make_request, get_stations, show_menu, add_to_config_file


@click.command()
@click.argument("location")
def add(location: str):
    """
    Add station data based on location to the config file.

    Stores the data as Dict[str, List[int, int]]

        {
            "location1": [uid1, uid2],
            "location2" :[uid32, uid46]
        }

    @TODO
    Before adding to the file:
    1. make sure the directory and the file to create is there.
    2. make sure teh entry is valid and let user select which location s/he wants to set.
    3. create a --all flag to set all the location presented in the result.
    """

    # Make search request to the API.
    data = make_request(location)

    # Get the name of stations and their uid from the response data.
    stations_data = get_stations(data)

    # Filter out just the stations.
    stations = [data.station for data in stations_data]

    # Allow user to select station to add to the config file.
    selected_station = show_menu(stations) if len(stations) > 1 else stations[0]

    # Get uid for selected station.
    station_uid = [
        data.uid for data in stations_data if data.station == selected_station
    ]

    # Add search query as key and uid as value.
    add_to_config_file(
        station_uid=station_uid, location=location, station=selected_station
    )
