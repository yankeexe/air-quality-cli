"""
Constants for the CLI.
"""
from pathlib import Path

BASE_URL = "https://api.waqi.info/search/?keyword={query}&token={API_KEY}"

HOME_DIR: str = str(Path.home())
CREDENTIAL_FILENAME: str = "creds"
STATIONS_FILENAME: str = "stations"
CONFIG_DIR: str = f"{HOME_DIR}/.aqi"

CONFIG_FILE: str = f"{CONFIG_DIR}/{STATIONS_FILENAME}"
CREDS_FILE = f"{CONFIG_DIR}/{CREDENTIAL_FILENAME}"
