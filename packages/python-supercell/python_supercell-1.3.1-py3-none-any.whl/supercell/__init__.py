"""
Weather Functions.
"""
# Standard Library
import datetime
import logging
from typing import Dict, List

# Third Party Code
from dateutil.parser import parse
from dateutil.tz import tzlocal
import requests

# Supercell Code
from supercell.models import Forecast, Observation

__version__ = "1.3.1"

WEATHER_URL = (
    "https://api.weather.com/v2/pws/observations/current?stationId="
    "{station_id}&format=json&units=e&apiKey={api_key}"
)
FORECAST_URL = (
    "https://api.weather.com/v3/wx/forecast/daily/5day?geocode="
    "{latitude},{longitude}&format=json&units=e&apiKey={api_key}"
    "&language=en-US"
)
NEAR_URL = (
    "https://api.weather.com/v3/location/near?format=json&geocode="
    "{latitude},{longitude}&product=postal&apiKey={api_key}"
)

logger = logging.getLogger(__name__)


def get_nearby(longitude: float, latitude: float, api_key: str) -> Dict:
    """
    Get a dictionary of nearby locations.
    """
    near_response = requests.get(
        NEAR_URL.format(latitude=latitude, longitude=longitude, api_key=api_key)
    )
    return near_response.json()


def get_forecasts(longitude: float, latitude: float, api_key: str) -> List[Forecast]:
    """
    Gets a list of forecasts for a location.
    """
    forecast_response = requests.get(
        FORECAST_URL.format(latitude=latitude, longitude=longitude, api_key=api_key)
    )
    forecasts = []
    forecast_data = forecast_response.json()
    for i, forecast_for_datetime_str in enumerate(forecast_data["validTimeLocal"]):
        try:
            forecast_for_datetime = parse(forecast_for_datetime_str)
        except ValueError:
            continue

        forecast_for_date = forecast_for_datetime.date()
        forecast_for_utc_offset = forecast_for_datetime.utcoffset()

        if forecast_for_utc_offset:
            forecast_for_utc_offset_seconds = int(
                forecast_for_utc_offset.total_seconds()
            )
        else:
            forecast_for_utc_offset_seconds = 0

        forecast_made = datetime.datetime.now(tzlocal())
        temperature_min = forecast_data["temperatureMin"][i]
        temperature_max = forecast_data["temperatureMax"][i]

        forecasts.append(
            Forecast(
                forecast_made_datetime=forecast_made,
                forecast_for_date=forecast_for_date,
                forecast_for_utc_offset_seconds=forecast_for_utc_offset_seconds,
                temperature_max=temperature_max,
                temperature_min=temperature_min,
                longitude=longitude,
                latitude=latitude,
            )
        )
    return forecasts


def get_station_weather(station_id: str, api_key: str) -> Observation:
    """
    Obtains an observation from a Weather Station.
    """
    weather_response = requests.get(
        WEATHER_URL.format(station_id=station_id, api_key=api_key)
    )
    return Observation(
        latitude=weather_response.json()["observations"][0]["lat"],
        longitude=weather_response.json()["observations"][0]["lon"],
        humidity=weather_response.json()["observations"][0]["humidity"],
        temperature=weather_response.json()["observations"][0]["imperial"]["temp"],
        windchill=weather_response.json()["observations"][0]["imperial"]["windChill"],
        windspeed=weather_response.json()["observations"][0]["imperial"]["windSpeed"],
        pressure=weather_response.json()["observations"][0]["imperial"]["pressure"],
        windgust=weather_response.json()["observations"][0]["imperial"]["windGust"],
        observed_at_str=weather_response.json()["observations"][0]["obsTimeUtc"] + "Z",
    )
