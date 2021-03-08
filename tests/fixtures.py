"""
Fixtures for testing
"""
from dataclasses import dataclass


@dataclass()
class StationData:
    empty_station_data = {"station": [], "aqi": None, "data": []}
    faulty_station_data = {"station": [], "aqi": None}
