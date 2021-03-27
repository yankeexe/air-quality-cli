"""
Fixtures for testing
"""
from dataclasses import dataclass

from air_quality_cli.constants import AirData


@dataclass()
class StationDataFixture:
    empty_station_data = {"station": [], "aqi": None, "data": []}
    faulty_station_data = {"station": [], "aqi": None}
    help_message = "No stations found in the location.:x:"


@dataclass
class GetAqiDataFixture:
    api_data = {
        "status": "ok",
        "data": [
            {
                "aqi": "356",
                "station": {
                    "name": "US Embassy, Phora Durbar, Kathmandu, Nepal",
                },
            },
            {
                "aqi": "348",
                "station": {
                    "name": "US Embassy, Kathmandu, Nepal",
                },
            },
        ],
    }

    faulty_api_data = {"status": "ok"}
    query = "xyz"
    error_message = (
        f"No air quality data found for search: [bold red]{query}[/bold red]"
    )

    data_store_values = [
        AirData(
            station="US Embassy, Phora Durbar, Kathmandu, Nepal", aqi="356"
        ),
        AirData(station="US Embassy, Kathmandu, Nepal", aqi="348"),
    ]
