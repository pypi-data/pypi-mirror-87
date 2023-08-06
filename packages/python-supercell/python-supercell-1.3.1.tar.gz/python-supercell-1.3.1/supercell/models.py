"""
Various Models.
"""
# Standard Library
import datetime
import random
from typing import Dict, Optional, Union

# Third Party Code
from dateutil.parser import parse
from dateutil.tz import tzutc


class Forecast(object):
    """
    A forecast.
    """

    identifier: int

    def __init__(
        self,
        forecast_for_date: Union[datetime.date, str],
        forecast_for_utc_offset_seconds: int,
        forecast_made_datetime: Union[datetime.datetime, str],
        temperature_min: float,
        temperature_max: float,
        longitude: float,
        latitude: float,
        identifier: Optional[int] = None,
    ) -> None:

        if isinstance(forecast_for_date, datetime.datetime):
            self._forecast_for_date = forecast_for_date.date()
        elif isinstance(forecast_for_date, datetime.date):
            self._forecast_for_date = forecast_for_date
        elif isinstance(forecast_for_date, str):
            self._forecast_for_date = parse(forecast_for_date).date()
        else:
            raise TypeError("Forecast for date must be a string or date.")

        self.forecast_for_utc_offset_seconds = int(forecast_for_utc_offset_seconds)

        if isinstance(forecast_made_datetime, datetime.datetime):
            self.forecast_made_datetime = forecast_made_datetime
        elif isinstance(forecast_made_datetime, str):
            self.forecast_made_datetime = parse(forecast_made_datetime)
        else:
            raise TypeError("Forecast made must be a string or datetime.")

        self.temperature_min = temperature_min and float(temperature_min) or None
        self.temperature_max = temperature_max and float(temperature_max) or None
        self.longitude = longitude
        self.latitude = latitude
        self.identifier = identifier or random.getrandbits(32)

    @property
    def forecast_made_date(self) -> datetime.date:
        return self.forecast_made_datetime.date()

    @property
    def forecast_made_date_float(self) -> float:
        """The date the forecast was made."""
        return datetime.datetime(
            year=self.forecast_made_datetime.year,
            month=self.forecast_made_datetime.month,
            day=self.forecast_made_datetime.day,
            tzinfo=tzutc(),
        ).timestamp()

    @property
    def forecast_for_date(self):
        return datetime.datetime(
            year=self._forecast_for_date.year,
            month=self._forecast_for_date.month,
            day=self._forecast_for_date.day,
            tzinfo=tzutc(),
        ).timestamp()

    @property
    def forecast_made_time(self) -> datetime.time:
        """The time the forecast was made"""
        return self.forecast_made_datetime.timetz()

    @property
    def forecast_made_time_int(self) -> int:
        return (
            self.forecast_made_datetime.hour * 100
        ) + self.forecast_made_datetime.minute

    @property
    def forecast_made_year(self) -> int:
        """The year the forecast was made"""
        return self.forecast_made_datetime.year

    @property
    def forecast_made_month(self) -> int:
        """The month the forecast was made"""
        return self.forecast_made_datetime.month

    @property
    def forecast_made_day(self) -> int:
        """The day the forecast was made"""
        return self.forecast_made_datetime.day

    @property
    def forecast_made_hour(self) -> int:
        """The hour the forecast was made"""
        return self.forecast_made_time.hour

    @property
    def forecast_made_minute(self) -> int:
        """The minute the forecast was made"""
        return self.forecast_made_time.minute

    @property
    def forecast_made_utc_offset_seconds(self) -> int:
        """The UTC offset of the location where the forecast was made."""
        offset = self.forecast_made_datetime.utcoffset()
        if offset:
            return int(offset.total_seconds())
        return 0

    @property
    def forecast_for_year(self) -> int:
        """The year the forecast is for"""
        return self._forecast_for_date.year

    @property
    def forecast_for_month(self) -> int:
        """The month the forecast is for"""
        return self._forecast_for_date.month

    @property
    def forecast_for_day(self) -> int:
        """The day the forecast is for"""
        return self._forecast_for_date.day

    @property
    def forecast_made_str(self) -> str:
        return str(self.forecast_made_datetime)

    @property
    def forecast_made(self) -> float:
        return self.forecast_made_datetime.timestamp()

    @property
    def forecast_for_date_str(self) -> str:
        return self._forecast_for_date.strftime("%Y-%m-%d")

    def to_dict(self) -> Dict:
        """A dictionary representation of the forecast"""
        return {
            "identifier": self.identifier,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "forecast_made_str": self.forecast_made_str,
            "forecast_made": self.forecast_made,
            "forecast_made_date": self.forecast_made_date_float,
            "forecast_made_time": self.forecast_made_time_int,
            "forecast_made_utc_offset_seconds": self.forecast_made_utc_offset_seconds,
            "forecast_for_date_str": self.forecast_for_date_str,
            "forecast_for_date": self.forecast_for_date,
            "forecast_for_utc_offset_seconds": self.forecast_for_utc_offset_seconds,
            "temperature_min": self.temperature_min,
            "temperature_max": self.temperature_max,
        }


class Observation(object):
    """An observation."""

    identifier: int
    humidity: float
    longitude: float
    latitude: float
    windchill: Optional[float]
    pressure: Optional[float]
    windgust: Optional[float]

    def __init__(
        self,
        temperature: float,
        humidity: float,
        longitude: float,
        latitude: float,
        observed_at_str: str,
        windchill: Optional[float] = None,
        windspeed: Optional[float] = None,
        pressure: Optional[float] = None,
        windgust: Optional[float] = None,
        identifier: Optional[int] = None,
    ) -> None:
        self.temperature = float(temperature)
        self.humidity = float(humidity)
        self.windchill = windchill and float(windchill) or None
        self.windspeed = windspeed and float(windspeed) or None
        self.pressure = pressure and float(pressure) or None
        self.windgust = windgust and float(windgust) or None
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self._observed_at = parse(observed_at_str)
        self.identifier = identifier or random.getrandbits(32)

    @property
    def observed_at_utc_offset_seconds(self) -> int:
        """The UTC offset of the location where the observation happened."""
        offset = self._observed_at.utcoffset()
        if offset:
            return int(offset.total_seconds())
        return 0

    @property
    def observed_at_str(self) -> str:
        return str(self._observed_at)

    @property
    def observed_at(self) -> float:
        return self._observed_at.timestamp()

    @property
    def observed_at_date(self) -> float:
        return datetime.datetime(
            year=self._observed_at.year,
            month=self._observed_at.month,
            day=self._observed_at.day,
            tzinfo=tzutc(),
        ).timestamp()

    @property
    def observed_at_time(self) -> int:
        return (self._observed_at.time().hour * 100) + self._observed_at.time().minute

    def to_dict(self) -> Dict:
        """A dictionary representation of the observation"""
        return {
            "identifier": self.identifier,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "observed_at_str": self.observed_at_str,
            "observed_at": self.observed_at,
            "observed_at_utc_offset_seconds": self.observed_at_utc_offset_seconds,
            "observed_at_date": self.observed_at_date,
            "observed_at_time": self.observed_at_time,
            "temperature": self.temperature,
            "humidity": self.humidity,
        }
