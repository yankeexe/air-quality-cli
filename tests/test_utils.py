"""
Unit Tests for utils.
"""
import pytest
from tests.fixtures import StationData
from air_quality_cli.utils import get_stations


class TestGetStations:
    @pytest.fixture(scope="class")
    def station_data_fixture(self):
        yield StationData()

    def test_get_stations_with_empty_data(self, station_data_fixture):
        with pytest.raises(SystemExit):
            assert get_stations(station_data_fixture.empty_station_data)

    def test_get_stations_with_key_error(self, station_data_fixture):
        with pytest.raises(KeyError):
            assert get_stations(station_data_fixture.faulty_station_data)
