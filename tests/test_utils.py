"""
Unit Tests for utils.
"""
import pytest
from unittest import mock

from tests.fixtures import GetAqiDataFixture, StationDataFixture
from air_quality_cli.utils import get_aqi_data, get_stations


class TestGetStations:
    @pytest.fixture(scope="class")
    def station_data_fixture(self):
        yield StationDataFixture()

    @mock.patch("air_quality_cli.utils.console", autospec=True)
    def test_get_stations__with_empty_data(
        self, mock_console, station_data_fixture
    ):
        """
        Test for no "data" field in the API return value raises SystemExit.
        """
        with pytest.raises(SystemExit):
            assert get_stations(station_data_fixture.empty_station_data)

        mock_console.print.assert_called_once_with(
            station_data_fixture.help_message
        )

    def test_get_stations__with_key_error(self, station_data_fixture):
        """
        Test raises KeyError when data node is not present in the API response.
        """
        with pytest.raises(KeyError):
            assert get_stations(station_data_fixture.faulty_station_data)


class TestGetAqiData:
    @pytest.fixture(scope="class")
    def get_aqi_data_fixture(self):
        yield GetAqiDataFixture()

    @mock.patch("air_quality_cli.utils.console", autospec=True)
    def test_get_aqi_data__with_empty_data(
        self, mock_console, get_aqi_data_fixture
    ):
        """
        Test for no "data" field in the API return value raises SystemExit.
        """
        with pytest.raises(SystemExit):
            assert get_aqi_data(
                get_aqi_data_fixture.faulty_api_data,
                get_aqi_data_fixture.query,
            )

        mock_console.print.assert_called_once_with(
            get_aqi_data_fixture.error_message
        )

    def test_get_aqi_data__with_valid_data(self, get_aqi_data_fixture):
        """
        Test for data_store returning the expected values from resposne payload.
        """
        expected = get_aqi_data_fixture.data_store_values
        got = get_aqi_data(
            get_aqi_data_fixture.api_data,
            get_aqi_data_fixture.query,
        )

        assert got == expected
