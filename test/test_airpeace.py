import json
import os
import sys

import pytest
from src.app_airpeace import AirPeaceFlightCheck

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Get the parent directory of the current script
parent_directory = os.path.dirname(current_script_path)

# Add the parent directory to the Python path
sys.path.append(parent_directory)


@pytest.fixture
def airpeace_instance():
    return AirPeaceFlightCheck("ABV", "LOS", "16.04.2024", "ROUND_TRIP", "20.04.2024")


def test_get_url(airpeace_instance):
    url = airpeace_instance.get_url()
    assert isinstance(url, str)
    assert "book-airpeace.crane.aero" in url


def test_capture_page_source(airpeace_instance):
    page_source = airpeace_instance.capture_page_source()
    assert isinstance(page_source, str)


def test_get_flight_info(airpeace_instance):
    flight_info = airpeace_instance.get_flight_info()
    flight_info_dict = json.loads(flight_info)
    assert isinstance(flight_info_dict, dict)
