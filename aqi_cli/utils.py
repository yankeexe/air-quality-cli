"""
Utility functions for the CLI
"""
import os
import sys
import json
from collections import namedtuple
from typing import Dict, List, NamedTuple, Tuple, Union


import requests
from rich import box
from rich.table import Table
from simple_term_menu import TerminalMenu

from aqi_cli import console
from aqi_cli.constants import (
    BASE_URL,
    CONFIG_FILE,
    CREDS_FILE,
    _CONFIG_DIR,
    TABLE_HEADERS,
    AQI_INFO_MAPPING,
)


def get_stations(data: Dict) -> List[NamedTuple]:
    """
    Get locations from the response.
    """
    Stations = namedtuple("Stations", ["uid", "station"])
    help_message = "No stations found in the location.:x:"

    data_node: List = data["data"]

    if not data_node:
        console.print(help_message)
        sys.exit()

    data_store = []
    for item in data_node:
        aqi = item["aqi"]
        # "-" represents no data in the payload
        # skip this value
        if aqi == "-":
            continue

        uid = item["uid"]
        station = item["station"]["name"]
        data_store.append(Stations(uid, station))

    # When aqi value for stations are "-" data_store will be empty.
    if not data_store:
        console.print(help_message)
        sys.exit()

    return data_store


def get_aqi_data(response_data: Dict, query: str) -> List[Tuple[str, str]]:
    """
    Grabs aqi data and station name from the response payload.

    Args:
        response_data: Response data from the API
    """
    data_node: List[Dict[str, str]] = response_data.get("data")
    AirData = namedtuple("AirData", ["station", "aqi"])

    # Check for empty data_node: []
    if not data_node:
        print(f"No data found for search result {query}")
        sys.exit()

    data_store: List[Tuple[str, str]] = []

    # Grab aqi value and station name from the response payload.
    for item in data_node:
        aqi = item["aqi"]

        # "-" represents no data in the payload
        # skip this value
        if aqi == "-":
            continue

        station = item["station"]["name"]
        data_package = AirData(station, aqi)
        data_store.append(data_package)

    return data_store


def check_config_file() -> Union[List, bool]:
    """
    Check for API keys in config file.
    Return if exists.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            # Remove Gew line character "\n"
            return [line.rstrip() for line in file][0]

    return False


def check_credential_file() -> Union[str, bool]:
    """
    Check for API TOKEN is in Envrionment variable
    else in config file.

    Return if exists.

    @TODO conflicts with `check_configs()` invariant. expects files and
     folders only but it checks env variable as well.
    """
    if (cred := os.environ.get("AQITOKEN")) is not None:
        return cred
    elif os.path.exists(CREDS_FILE):
        with open(CREDS_FILE) as cred:
            return cred.readline()

    return False


def add_credential(credential: str):
    """
    Store creds in .aqi/creds
    """
    # Create a config directory if it doesn't exist.
    if not os.path.exists(_CONFIG_DIR):
        os.mkdir(_CONFIG_DIR)

    # Write credentials to the file.
    # @TODO add hashing to encrypt the keys.
    with open(f"{CREDS_FILE}", "w+") as cred:
        cred.write(credential.strip())

    console.print(
        f"Credentials saved to [bold blue]{CREDS_FILE}[/bold blue]:white_check_mark:",
        style="bold green",
    )


def make_request(query: str) -> Dict[str, str]:
    """
    Make an API request.

    @TODO handle HTTP exceptions.
    """
    token = check_credential_file()

    if not token:
        console.print(
            ":key: [bold red]No API token found, use [green]`air init`[/green] to enter API key.[/bold red]"
        )
        sys.exit()

    r = requests.get(BASE_URL.format(query=query, API_KEY=token))

    return r.json()


def show_menu(data: List[str]) -> str:
    """
    Show interactive menu and return the selected data.
    """
    terminal_menu = TerminalMenu(data)
    menu_entry_index = terminal_menu.show()

    # Check for None value when user presses `esc` or `ctrl + c`
    if menu_entry_index is None:
        raise KeyboardInterrupt

    return data[menu_entry_index]


def check_configs():
    """
    checks if both the config files are present.

    Config files:
        - credential: ~/.aqi/creds
        - saved locations: ~/.aqi/config

    """
    if not os.path.exists(_CONFIG_DIR) or not check_credential_file:
        console.print(
            "You have not initialized the app, [bold green]use `air init` to add token[/bold green]"
        )
        sys.exit()


def add_to_config_file(*, station_uid: List[int], location: str, station: str):
    """
    Add station to config file.
    """
    check_configs()
    help_message = f"Successfully added {station}!"

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w+"):
            pass

    with open(CONFIG_FILE, "r+") as file:

        data = file.readline()

        if not data:
            value = {location: station_uid}
            json.dump(value, file)

            console.print(help_message)
            sys.exit()

        data_dict = json.loads(data)

        if location not in data_dict:
            data_dict[location] = station_uid
        elif station_uid[0] in data_dict[location]:
            console.print(f"Station: {station} already exists.")
            sys.exit()
        else:
            data_dict[location].append(station_uid[0])

        file.seek(0)
        json.dump(data_dict, file)

    console.print(help_message)


def show_table(data):
    """
    Show table to preview data.
    """
    table = Table(
        *TABLE_HEADERS,
        header_style="bold",
        title="Air Quality Index",
        title_style="bold black on white",
        box=box.ROUNDED,
        show_lines=True,
    )

    for row in data:
        table.add_row(*row)

    console.print(table)


def info_mapper():
    """
    Maps the aqi value to its information.
    """
    data = {}
    for range, info in AQI_INFO_MAPPING:
        for index in range:
            data[index] = info

    return data


def create_table_payload(aqi_data: List[NamedTuple]):
    """
    Create payload compatible with table.
    """
    data = []
    info_mapping = info_mapper()
    for location, aqi in aqi_data:
        data_info = info_mapping[int(aqi)]
        data.append((location, aqi, *data_info))

    return data
