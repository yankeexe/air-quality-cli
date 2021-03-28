"""
Add command for the CLI.
"""
import click
from air_quality_cli.utils import (
    make_request,
    get_stations,
    show_menu,
    add_to_config_file,
)


@click.command()
@click.argument("location")
def add(location: str):
    """
    Add station data based on location to the config file.

    Stores the data as Dict[str, List[int, Dict[str, Union[str, int]]]]

        {
            "location1": [
                { "name" : "station_name1", "uid" : "uid01", },
                { "name" : "station_name2", "uid" : "uid02", },
            ],
            "location2": [
                { "name" : "station_name3", "uid" : "uid03", },
                { "name" : "station_name4", "uid" : "uid04", },
            ],
        }
    """

    # Make search request to the API.
    data = make_request(location)

    # Get the name of stations and their uid from the response data.
    stations_data = get_stations(data)

    # Filter out just the stations.
    stations = [data.station for data in stations_data]

    # Allow user to select station to add to the config file.
    selected_station = (
        show_menu(stations) if len(stations) > 1 else stations[0]
    )

    # Get uid for selected station.
    station_uid = [
        data.uid for data in stations_data if data.station == selected_station
    ]

    # Add search query as key and uid as value.
    add_to_config_file(
        station_uid=station_uid, location=location, station=selected_station
    )
