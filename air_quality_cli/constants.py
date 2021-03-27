"""
Constants for the CLI.
"""
from pathlib import Path
from collections import namedtuple


BASE_URL = "https://api.waqi.info/search/?keyword={query}&token={API_KEY}"

_HOME_DIR: str = str(Path.home())
_CREDENTIAL_FILENAME: str = "creds"
_STATIONS_FILENAME: str = "stations"
_CONFIG_DIR: str = f"{_HOME_DIR}/.aqi"

CONFIG_FILE: str = f"{_CONFIG_DIR}/{_STATIONS_FILENAME}"
CREDS_FILE = f"{_CONFIG_DIR}/{_CREDENTIAL_FILENAME}"

TOKEN_HELP_MSG = (
    "Get your token here: https://aqicn.org/data-platform/token/#/\n"
)

TABLE_HEADERS = ["Location", "AQI", "Level", "Implications", "Cautionary"]

Info = namedtuple("Info", ["level", "implications", "cautionary"])
AirData = namedtuple("AirData", ["station", "aqi"])
Stations = namedtuple("Stations", ["uid", "station"])


AQI_INFO_MAPPING = [
    (
        range(0, 51),
        Info(
            "[bold green]Good[/bold green]",
            "Air quality is considered satisfactory, and air pollution poses little or no risk",
            "-",
        ),
    ),
    (
        range(51, 101),
        Info(
            "[bold yellow]Moderate[/bold yellow]",
            "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.	",
            "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
        ),
    ),
    (
        range(101, 151),
        Info(
            "[bold magenta]Unhealthy for Sensitive Groups[/bold magenta]",
            "Members of sensitive groups may experience health effects. The general public is not likely to be affected",
            "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.",
        ),
    ),
    (
        range(151, 201),
        Info(
            "[bold red]Unhealthy[/bold red]",
            "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects",
            "Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion",
        ),
    ),
    (
        range(201, 301),
        Info(
            "[bold purple]Very Unhealthy[/bold purple]",
            "Health warnings of emergency conditions. The entire population is more likely to be affected.",
            "Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion.",
        ),
    ),
    (
        range(301, 501),
        Info(
            "[bold brown]Hazardous[/bold brown]",
            "Health alert: everyone may experience more serious health effects",
            "Everyone should avoid all outdoor exertion",
        ),
    ),
]


NO_AQI = Info("No data received from the station.", "-", "-")

AQI_COLOR_MAPPING = {
    "Good": "white on green",
    "Moderate": "white on yellow",
    "Unhealthy for Sensitive Groups": "white on orange",
    "Unhealthy": "white on red",
    "Very Unhealthy": "white on purple",
    "Hazardous": "white on brown",
}
