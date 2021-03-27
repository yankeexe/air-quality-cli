"""
Utility functions for the CLI
"""
import os
import sys
import json
import concurrent.futures
from typing import Dict, List, NamedTuple, Tuple, Union

import requests
from rich import box
from rich.table import Table
from simple_term_menu import TerminalMenu

from air_quality_cli import console
from air_quality_cli.constants import (
    BASE_URL,
    CONFIG_FILE,
    CREDS_FILE,
    NO_AQI,
    _CONFIG_DIR,
    TABLE_HEADERS,
    AQI_INFO_MAPPING,
    AirData,
    Stations,
)


def get_stations(data: Dict) -> List[NamedTuple]:
    """
    Get stations from the response payload.
    """
    help_message = "No stations found in the location.:x:"

    data_node: List = data["data"]

    if not data_node:
        console.print(help_message)
        sys.exit()

    data_store = []
    for item in data_node:
        aqi = item["aqi"]

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
        response_data: Response data from the API.
        query: search query from user.
    """
    data_store: List[Tuple[str, str]] = []

    data_node: List[Dict[str, str]] = response_data.get("data")

    # Check for empty data_node: []
    if not data_node:
        console.print(
            f"No air quality data found for search: [bold red]{query}[/bold red]"
        )
        sys.exit()

    # Grab aqi value and station name from the response payload.
    for item in data_node:
        aqi = item["aqi"]

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

    @TODO
    Decide to keep or remove taking values from env.
    Other checks look for `creds` file.
    """
    if (cred := os.environ.get("AQITOKEN")) is not None:
        return cred
    elif os.path.exists(CREDS_FILE):
        with open(CREDS_FILE) as cred:
            return cred.readline().strip()

    return False


def add_credential(credential: str):
    """
    Store creds in .aqi/creds
    """
    # Create a config directory if it doesn't exist.
    if not os.path.exists(_CONFIG_DIR):
        os.mkdir(_CONFIG_DIR)

    # @TODO add hashing to encrypt the keys.
    # Write credentials to the file.
    with open(f"{CREDS_FILE}", "w+") as cred:
        cred.write(credential.strip())

    console.print(
        f"Credentials saved to [bold blue]{CREDS_FILE}[/bold blue]:white_check_mark:",
        style="bold green",
    )


def make_request(query: str) -> Dict[str, str]:
    """
    Make an API request.

    Args:
        query: search query from user input.
    """
    token = check_credential_file()

    if not token:
        console.print(
            ":key: [bold red]No API token found, use [green]`air init`[/green] to enter API key.[/bold red]"
        )
        sys.exit()

    try:
        response = requests.get(
            BASE_URL.format(query=query, API_KEY=token),
            timeout=10,
        )
        response.raise_for_status()

        if response.json().get("status") == "error":
            raise requests.exceptions.HTTPError

    except requests.exceptions.HTTPError:
        error = response.json().get("data")
        console.print(
            f"Error: {error}.:x:",
            style="bold red",
        )

        sys.exit()
    except requests.exceptions.ConnectionError:
        console.print("[bold red]No connection:x:[/bold red]")
        sys.exit()
    except requests.exceptions.RequestException:
        console.print(
            "An error has occcured. Please try again later or open an issue on GitHub.:x:",
            style="bold red",
        )
        sys.exit()
    except requests.exceptions.ReadTimeout:
        console.print(
            "Network connection timeout.:construction:", style="bold red"
        )

        sys.exit()

    except Exception:
        error_base = response.json().get("errors")[0]

        console.print(
            f"Error: {error_base.get('message')}:x:",
            style="bold red",
        )

        sys.exit()

    return response.json()


def show_menu(data: List[str]) -> str:
    """
    Show interactive menu and return the selected data.

    Args:
        data: items to view in the menu.
    """
    terminal_menu = TerminalMenu(data)
    menu_entry_index = terminal_menu.show()

    # Check for None value when user presses `esc` or `ctrl + c`
    if menu_entry_index is None:
        raise KeyboardInterrupt

    return data[menu_entry_index]


def check_configs():
    """
    Checks if both the config directory and credential config are present.
    """
    if not os.path.exists(_CONFIG_DIR) or not check_credential_file:
        console.print(
            "You have not initialized the app, [bold green]use `air init` to add token[/bold green]"
        )
        sys.exit()


def add_to_config_file(*, station_uid: List[int], location: str, station: str):
    """
    Add station to config file.

    Args:
        * : all arguments after this should be keyword arguments.

        station_uid: unique identifier for the station.
        location: search query entered by user.
        station: name of the station.
    """
    help_message = f"Successfully added {station}!"

    # Check for both config folder and credentials file.
    check_configs()

    # Create stations config file if it does not exist.
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w+"):
            pass

    # Add search query and uid to config dictionary.
    with open(CONFIG_FILE, "r+") as file:
        data = file.readline()

        # If config file empty.
        if not data:
            value = {location: station_uid}
            json.dump(value, file)

            console.print(help_message)
            sys.exit()

        data_dict = json.loads(data)

        # If key for search location does not exist, add station based on it.
        # Else check if uid for the search query already exists.
        # Else assume the key for the search query exists; append uid to its value (List).
        if location not in data_dict:
            data_dict[location] = station_uid
        elif station_uid[0] in data_dict[location]:
            console.print(f"Station: {station} already exists.")
            sys.exit()
        else:
            data_dict[location].append(station_uid[0])

        # Rewrite the config dictionary with updated value.
        file.seek(0)
        json.dump(data_dict, file)

    console.print(help_message)


def show_table(data: List[Tuple]):
    """
    Show table to preview data.

    Args:
        data: Air Quality information.
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
    Creates a mapping expanding the range(key) used for aqi values in AQI_INFO_MAPPING.
    Repeats the value for that range of keys.
    """
    data = {}
    for range, info in AQI_INFO_MAPPING:
        for index in range:
            data[index] = info

    return data


def create_table_payload(aqi_data: List[NamedTuple]) -> List[Tuple]:
    """
    Create payload compatible with table with all aqi info.

    Args:
        aqi_data: station and aqi value extracted from search query.
    """
    data = []

    # Create a mapping with aqi value and their information.
    info_mapping = info_mapper()

    # Grab information for the aqi value.
    # Create a tuple with aqi_data and information based on aqi value.
    for location, aqi in aqi_data:
        if aqi == "-":
            data.append((location, aqi, *NO_AQI))
        else:
            data_info = info_mapping[int(aqi)]
            data.append((location, aqi, *data_info))

    return data


def get_config_stations() -> Dict[str, List[int]]:
    """
    Reads the config dictionary from the file.
    """
    help_msg = "You have not saved any stations, use [bold green]`air add <location>`[/bold green] to save a station!"

    if not os.path.exists(_CONFIG_DIR):
        console.print(
            "App is not initialized. Use [bold green]`air init`[/bold green] to get started!"
        )
        sys.exit()

    if not os.path.exists(CONFIG_FILE):
        console.print(help_msg)
        sys.exit()

    with open(CONFIG_FILE, "r") as file:
        data = json.loads(file.readline())

        if not data:
            console.print(help_msg)
            sys.exit()

        return data


def concurrent_requests(config_data: Dict[str, List[int]]) -> List:
    """
    Send concurrent requests to the API.
    """
    aqi_response: List = []
    queries = config_data.keys()

    # Send concurrent requests to the API.
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        submit = [
            executor.submit(
                make_request,
                query,
            )
            for query in queries
        ]

        for future in concurrent.futures.as_completed(submit):
            # Ignore empty values.
            if not future.result():
                continue

            aqi_response.append(future.result()["data"])

    # spinner.succeed("Parsing complete.")

    return aqi_response


def filter_show_stations(data: List[Dict[str, List[int]]], config_data):
    """
    Filter the stations to show based on the values in config dictionary.
    """
    data_store = []

    station_uids = list(config_data.values())
    flatten_uids = [item for sublist in station_uids for item in sublist]

    # Load = data returned from concurrent request.
    for load in data:
        for item in load:
            if item["uid"] in flatten_uids:
                aqi = item["aqi"]
                station = item["station"]["name"]
                data_store.append(AirData(station, aqi))

    return data_store
