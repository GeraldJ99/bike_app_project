# File: tests/test_flask_app.py (Pytest version)

import pytest
from unittest.mock import patch, MagicMock
from app import app

# Fixture to initialize test client
@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@patch('static.jcddecaux.get_bike_data')
def test_stations_route(mock_get_bike_data, client):
    # Mock bike station data
    mock_get_bike_data.return_value = {"stations": ["Test Station"]}
    response = client.get('/stations')
    assert response.status_code == 200
    assert response.get_json() == {"stations": ["Test Station"]}

@patch('static.weatherscrap.get_weather_data')
def test_weather_route(mock_get_weather_data, client):
    # Mock weather data
    mock_get_weather_data.return_value = {"temp": 23}
    response = client.get('/weather')
    assert response.status_code == 200
    assert response.get_json() == {"temp": 23}

def test_availability_route_no_station(client):
    # Missing station parameter should return 400
    response = client.get('/availability')
    assert response.status_code == 400
    assert "error" in response.get_json()

@patch('builtins.open')
@patch('csv.DictReader')
def test_availability_route_valid_station(mock_dict_reader, mock_open, client):
    # Simulate CSV return for station availability
    mock_dict_reader.return_value = [
        {'hour': '09', 'station_number': '101', 'available_bikes': '5'}
    ]
    response = client.get('/availability?station=101')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
