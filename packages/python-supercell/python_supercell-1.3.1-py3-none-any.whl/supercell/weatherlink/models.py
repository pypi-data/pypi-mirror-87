# Standard Library
import datetime
import random
from typing import Dict, List, Optional

# Third Party Code
from bitstring import BitStream
from dateutil.tz import tzlocal
import ephem

# Supercell Code
from supercell.weatherlink.exceptions import BadCRC
from supercell.weatherlink.utils import crc16, CRC16_TABLE, make_time

FORECAST_RULES = [
    "Mostly clear and cooler.",
    "Mostly clear with little temperature change.",
    "Mostly clear for 12 hours with little temperature change.",
    "Mostly clear for 12 to 24 hours and cooler.",
    "Mostly clear with little temperature change.",
    "Partly cloudy and cooler.",
    "Partly cloudy with little temperature change.",
    "Partly cloudy with little temperature change.",
    "Mostly clear and warmer.",
    "Partly cloudy with little temperature change.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 24 to 48 hours.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds with little temperature change. Precipitation possible within 24 hours.",
    "Mostly clear with little temperature change.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds with little temperature change. Precipitation possible within 12 hours.",
    "Mostly clear with little temperature change.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 24 hours.",
    "Mostly clear and warmer. Increasing winds.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 hours. Increasing winds.",
    "Mostly clear and warmer. Increasing winds.",
    "Increasing clouds and warmer.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 hours. Increasing winds.",
    "Mostly clear and warmer. Increasing winds.",
    "Increasing clouds and warmer.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 hours. Increasing winds.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly clear and warmer. Precipitation possible within 48 hours.",
    "Mostly clear and warmer.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds with little temperature change. Precipitation possible within 24 to 48 hours.",
    "Increasing clouds with little temperature change.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 to 24 hours.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 to 24 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 to 24 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 6 to 12 hours.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 6 to 12 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 to 24 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation possible within 12 hours.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and warmer. Precipitation likley.",
    "Clearing and cooler. Precipitation ending within 6 hours.",
    "Partly cloudy with little temperature change.",
    "Clearing and cooler. Precipitation ending within 6 hours.",
    "Mostly clear with little temperature change.",
    "Clearing and cooler. Precipitation ending within 6 hours.",
    "Partly cloudy and cooler.",
    "Partly cloudy with little temperature change.",
    "Mostly clear and cooler.",
    "Clearing and cooler. Precipitation ending within 6 hours.",
    "Mostly clear with little temperature change.",
    "Clearing and cooler. Precipitation ending within 6 hours.",
    "Mostly clear and cooler.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds with little temperature change. Precipitation possible within 24 hours.",
    "Mostly cloudy and cooler. Precipitation continuing.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation likely.",
    "Mostly cloudy with little temperature change. Precipitation continuing.",
    "Mostly cloudy with little temperature change. Precipitation likely.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible and windy within 6 hours.",
    "Increasing clouds with little temperature change. Precipitation possible and windy within 6 hours.",
    "Mostly cloudy and cooler. Precipitation continuing. Increasing winds.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation likely. Increasing winds.",
    "Mostly cloudy with little temperature change. Precipitation continuing. Increasing winds.",
    "Mostly cloudy with little temperature change. Precipitation likely. Increasing winds.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 12 to 24 hours possible wind shift to the W NW or N.",
    "Increasing clouds with little temperature change. Precipitation possible within 12 to 24 hours possible wind "
    "shift to the W NW or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 6 hours possible wind shift to the W NW or N.",
    "Increasing clouds with little temperature change. Precipitation possible within 6 hours possible wind shift to "
    "the W NW or N.",
    "Mostly cloudy and cooler. Precipitation ending within 12 hours possible wind shift to the W NW or N.",
    "Mostly cloudy and cooler. Possible wind shift to the W NW or N.",
    "Mostly cloudy with little temperature change. Precipitation ending within 12 hours possible wind shift to the W "
    "NW or N.",
    "Mostly cloudy with little temperature change. Possible wind shift to the W NW or N.",
    "Mostly cloudy and cooler. Precipitation ending within 12 hours possible wind shift to the W NW or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation possible within 24 hours possible wind shift to the W NW or N.",
    "Mostly cloudy with little temperature change. Precipitation ending within 12 hours possible wind shift to the W "
    "NW or N.",
    "Mostly cloudy with little temperature change. Precipitation possible within 24 hours possible wind shift to the "
    "W NW or N.",
    "Clearing cooler and windy. Precipitation ending within 6 hours.",
    "Clearing cooler and windy.",
    "Mostly cloudy and cooler. Precipitation ending within 6 hours. Windy with possible wind shift to the W NW or N.",
    "Mostly cloudy and cooler. Windy with possible wind shift to the W NW or N.",
    "Clearing cooler and windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy with little temperature change. Precipitation possible within 12 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 12 hours possibly heavy at times. Windy.",
    "Mostly cloudy and cooler. Precipitation ending within 6 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation possible within 12 hours. Windy.",
    "Mostly cloudy and cooler. Precipitation ending in 12 to 24 hours.",
    "Mostly cloudy and cooler.",
    "Mostly cloudy and cooler. Precipitation continuing possible heavy at times. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation possible within 6 to 12 hours. Windy.",
    "Mostly cloudy with little temperature change. Precipitation continuing possibly heavy at times. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy with little temperature change. Precipitation possible within 6 to 12 hours. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds with little temperature change. Precipitation possible within 12 hours possibly heavy at "
    "times. Windy.",
    "Mostly cloudy and cooler. Windy.",
    "Mostly cloudy and cooler. Precipitation continuing possibly heavy at times. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation likely possibly heavy at times. Windy.",
    "Mostly cloudy with little temperature change. Precipitation continuing possibly heavy at times. Windy.",
    "Mostly cloudy with little temperature change. Precipitation likely possibly heavy at times. Windy.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 6 hours. Windy.",
    "Increasing clouds with little temperature change. Precipitation possible within 6 hours. Windy",
    "Increasing clouds and cooler. Precipitation continuing. Windy with possible wind shift to the W NW or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation likely. Windy with possible wind shift to the W NW or N.",
    "Mostly cloudy with little temperature change. Precipitation continuing. Windy with possible wind shift to the W "
    "NW or N.",
    "Mostly cloudy with little temperature change. Precipitation likely. Windy with possible wind shift to the W NW "
    "or N.",
    "Increasing clouds and cooler. Precipitation possible within 6 hours. Windy with possible wind shift to the W NW "
    "or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 6 hours possible wind shift to the W NW or N.",
    "Increasing clouds with little temperature change. Precipitation possible within 6 hours. Windy with possible "
    "wind shift to the W NW or N.",
    "Increasing clouds with little temperature change. Precipitation possible within 6 hours possible wind shift to "
    "the W NW or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 6 hours. Windy with possible wind shift to the W NW "
    "or N.",
    "Increasing clouds with little temperature change. Precipitation possible within 6 hours. Windy with possible "
    "wind shift to the W NW or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Increasing clouds and cooler. Precipitation possible within 12 to 24 hours. Windy with possible wind shift to "
    "the W NW or N.",
    "Increasing clouds with little temperature change. Precipitation possible within 12 to 24 hours. Windy with "
    "possible wind shift to the W NW or N.",
    "Mostly cloudy and cooler. Precipitation possibly heavy at times and ending within 12 hours. Windy with possible "
    "wind shift to the W NW or N.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation possible within 6 to 12 hours possibly heavy at times. Windy with "
    "possible wind shift to the W NW or N.",
    "Mostly cloudy with little temperature change. Precipitation ending within 12 hours. Windy with possible wind "
    "shift to the W NW or N.",
    "Mostly cloudy with little temperature change. Precipitation possible within 6 to 12 hours possibly heavy at "
    "times. Windy with possible wind shift to the W NW or N.",
    "Mostly cloudy and cooler. Precipitation continuing.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation likely. Windy with possible wind shift to the W NW or N.",
    "Mostly cloudy with little temperature change. Precipitation continuing.",
    "Mostly cloudy with little temperature change. Precipitation likely.",
    "Partly cloudy with little temperature change.",
    "Mostly clear with little temperature change.",
    "Mostly cloudy and cooler. Precipitation possible within 12 hours possibly heavy at times. Windy.",
    "FORECAST REQUIRES 3 HOURS OF RECENT DATA",
    "Mostly clear and cooler.",
    "Mostly clear and cooler.",
    "Mostly clear and cooler.",
    "Unknown forecast rule."]

BAR_TREND_CODE_FALLING_RAPIDLY = -60
BAR_TREND_TEXT_FALLING_RAPIDLY = "Falling Rapidly"

BAR_TREND_CODE_FALLING_SLOWLY = -20
BAR_TREND_TEXT_FALLING_SLOWLY = "Falling Slowly"

BAR_TREND_CODE_STABLE = 0
BAR_TREND_TEXT_STABLE = "Stable"

BAR_TREND_CODE_RISING_SLOWLY = 20
BAR_TREND_TEXT_RISING_SLOWLY = "Rising Slowly"

BAR_TREND_CODE_RISING_RAPIDLY = 60
BAR_TREND_TEXT_RISING_RAPIDLY = "Rising Rapidly"

BAR_TREND_TEXT = dict((
    (BAR_TREND_CODE_FALLING_RAPIDLY, BAR_TREND_TEXT_FALLING_RAPIDLY),
    (BAR_TREND_CODE_FALLING_SLOWLY, BAR_TREND_TEXT_FALLING_SLOWLY),
    (BAR_TREND_CODE_STABLE, BAR_TREND_TEXT_STABLE),
    (BAR_TREND_CODE_RISING_SLOWLY, BAR_TREND_TEXT_RISING_SLOWLY),
    (BAR_TREND_CODE_RISING_RAPIDLY, BAR_TREND_TEXT_RISING_RAPIDLY),
))

LOOP_RECORD_SIZE_BYTES = 99
LOOP_RECORD_SIZE_BITS = LOOP_RECORD_SIZE_BYTES * 8

REVISION_A = "A"
REVISION_B = "B"

LOOP_HEADER = b"LOOP"

LOOP2_PACKET_TYPE = "LOOP2"
LOOP_PACKET_TYPE = "LOOP"

LUNATION_LOOKUP = {
    0.05: "New Moon",
    0.15: "Crescent",
    0.25: "First Quarter",
    0.45: "Gibbous",
    0.55: "Full Moon",
    0.65: "Gibbous",
    0.85: "Last Quarter",
    0.95: "Crescent",
    1.00: "New Moon"
}


WIND_DIRECTION_LOOKUP = {
    10: "N",
    35: "NNE",
    55: "NE",
    80: "NEE",
    110: "E",
    125: "SEE",
    145: "SE",
    170: "SSE",
    190: "S",
    215: "SSW",
    235: "SW",
    260: "SWW",
    280: "W",
    305: "NWW",
    325: "NW",
    350: "NNW",
    360: "N"
}

FORECAST_ICONS_LOOKUP = {
    1: "Rain within 12 hrs",
    2: "Cloudy",
    4: "Cloud + Sunny",
    8: "Sunny",
    16: "Snow within 12hrs"
}


def _lunation_text(lunation: float) -> str:
    """Converts the lunation value to a string."""
    if lunation < 0 or lunation > 1.0:
        raise ValueError("Lunation must be between 0.0 - 1.0")

    if lunation < 0.5:
        direction = "Waxing"
    else:
        direction = "Waning"

    for lunation_value, lunation_text in LUNATION_LOOKUP.items():
        if lunation >= lunation_value:
            continue
        break

    return "{text} ({direction})".format(
        text=lunation_text,
        direction=direction
    )


def _wind_direction_text(wind_direction: int) -> str:
    """Converts the wind direction value to text."""
    if wind_direction < 0 or wind_direction > 360:
        raise ValueError("Wind direction (%s) must be between 0 - 360" % (wind_direction))
    for wind_direction_value, wind_direction_text in WIND_DIRECTION_LOOKUP.items():
        if wind_direction >= wind_direction_value:
            continue
        break
    return wind_direction_text


def _forecast_icons_text(forecast_icons: int) -> List[str]:
    if forecast_icons < 0 or forecast_icons > 31:
        raise ValueError("Forecast icons must be between 0 - 31.")
    return [
        forecast_icon_text
        for bit_position, forecast_icon_text
        in FORECAST_ICONS_LOOKUP.items()
        if ((forecast_icons & bit_position) == bit_position)
    ]


def get_phase_on_day(year: int, month: int, day: int) -> float:
    """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
    date = ephem.Date(datetime.date(year, month, day))
    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)
    lunation = (date - pnm) / (nnm - pnm)
    return lunation


class StationObservation(object):
    """A station observation"""
    bar_trend: int
    barometer: float
    inside_temperature: float
    inside_humidity: float
    outside_temperature: float
    outside_humidity: float
    wind_speed: int
    ten_min_avg_wind_speed: int
    wind_direction: int
    rain_rate: int
    console_battery_voltage: float
    forecast_icons: int
    forecast_rule_number: int
    sunrise: datetime.time
    sunset: datetime.time
    observation_made_at: datetime.datetime
    identitier: int

    def __init__(self,
                 bar_trend: int,
                 barometer: float,
                 inside_temperature: float,
                 inside_humidity: float,
                 outside_temperature: float,
                 outside_humidity: float,
                 wind_speed: int,
                 ten_min_avg_wind_speed: int,
                 wind_direction: int,
                 rain_rate: int,
                 console_battery_voltage: float,
                 forecast_icons: int,
                 forecast_rule_number: int,
                 sunrise: datetime.time,
                 sunset: datetime.time,
                 observation_made_at: Optional[datetime.datetime] = None,
                 identifier: Optional[int] = None
                 ) -> None:
        self.bar_trend = int(bar_trend)
        self.barometer = float(barometer)
        self.inside_temperature = float(inside_temperature)
        self.inside_humidity = float(inside_humidity)
        self.outside_temperature = float(outside_temperature)
        self.outside_humidity = float(outside_humidity)
        self.wind_speed = int(wind_speed)
        self.ten_min_avg_wind_speed = int(ten_min_avg_wind_speed)
        self.wind_direction = int(wind_direction)
        self.rain_rate = int(rain_rate)
        self.console_battery_voltage = float(console_battery_voltage)
        self.forecast_icons = int(forecast_icons)
        self.forecast_rule_number = int(forecast_rule_number)
        self.sunrise = sunrise
        self.sunset = sunset
        self.observation_made_at = observation_made_at or datetime.datetime.now(tzlocal())
        self.lunation = get_phase_on_day(
            self.observation_made_at.year,
            self.observation_made_at.month,
            self.observation_made_at.day)
        self.identifier = identifier or random.getrandbits(32)

    def lunation_text(self) -> str:
        return _lunation_text(self.lunation)

    def wind_direction_text(self) -> str:
        """Produces a string description of the wind direction."""
        return _wind_direction_text(self.wind_direction)

    def bar_trend_text(self) -> str:
        """Returns the string version of the bar trend."""
        return BAR_TREND_TEXT[self.bar_trend]

    def forecast_icons_text(self) -> List[str]:
        return _forecast_icons_text(self.forecast_icons)

    def forecast_text(self) -> str:
        """Returns the string version of the forecast rule."""
        return FORECAST_RULES[self.forecast_rule_number]

    def to_dict(self) -> Dict:
        """A dictionary representation of the observation."""
        return {
            "bar_trend": self.bar_trend,
            "bar_trend_text": self.bar_trend_text(),
            "barometer": self.barometer,
            "inside_temperature": self.inside_temperature,
            "inside_humidity": self.inside_humidity,
            "outside_temperature": self.outside_temperature,
            "outside_humidity": self.outside_humidity,
            "wind_speed": self.wind_speed,
            "ten_min_avg_wind_speed": self.ten_min_avg_wind_speed,
            "wind_direction": self.wind_direction,
            "wind_direction_text": self.wind_direction_text(),
            "rain_rate": self.rain_rate,
            "console_battery_voltage": self.console_battery_voltage,
            "forecast_icons": self.forecast_icons,
            "forecast_icons_text": self.forecast_icons_text(),
            "forecast_rule_number": self.forecast_rule_number,
            "forecast_text": self.forecast_text(),
            "sunrise": self.sunrise.isoformat(),
            "sunset": self.sunset.isoformat(),
            "lunation": self.lunation,
            "lunation_text": self.lunation_text(),
            "observation_made_at": self.observation_made_at,
            "identifier": self.identifier
        }

    @classmethod
    def validate_record(cls, record_bitstream: BitStream) -> None:
        """Validates a record."""
        if len(record_bitstream) != LOOP_RECORD_SIZE_BITS:
            raise ValueError("Records should be %d bytes in length." % LOOP_RECORD_SIZE_BYTES)
        if crc16(record_bitstream, 0, CRC16_TABLE) != 0:
            raise BadCRC()

    @classmethod
    def validate_packet_type(cls, record_bitstream: BitStream) -> None:
        """Validates the packet type."""
        packet_type = record_bitstream.read(8).int and "LOOP2" or "LOOP"
        if packet_type == LOOP2_PACKET_TYPE:
            raise ValueError("LOOP2 Packet not yet supported.")

    @classmethod
    def init_with_bytes(cls, record_bytes: bytes, identifier: Optional[int] = None,
                        observation_made_at: Optional[datetime.datetime] = None):
        """Creates a new Station Observation from record of bytes."""
        record_bitstream = BitStream(record_bytes)
        cls.validate_record(record_bitstream)
        # Set to position four
        record_bitstream.pos = 24
        # Awkwardly positioned bar trend
        bar_trend = record_bitstream.read(8).intle
        cls.validate_packet_type(record_bitstream)
        # Skip 2 bytes
        record_bitstream.read(16)

        barometer = record_bitstream.read(16).uintle / 1000.0
        inside_temperature = record_bitstream.read(16).intle / 10.0
        inside_humidity = record_bitstream.read(8).uintle
        outside_temperature = record_bitstream.read(16).intle / 10.0
        wind_speed = record_bitstream.read(8).uintle
        ten_min_avg_wind_speed = record_bitstream.read(8).uintle
        wind_direction = record_bitstream.read(16).uintle  # 0º = None, 90º = E, 180 = S, 270 = W, 360 = N

        # Skip "extra temperatures"
        record_bitstream.read(56)  # Each byte is a one extra temperature value in whole degrees F
        # with # an offset  of 90 degrees. 0 = -90, 100 = 10, 169 = 79
        # Skip soil temperatures
        record_bitstream.read(32)
        # Skip leaf temperatures
        record_bitstream.read(32)

        outside_humidity = record_bitstream.read(8).uintle

        # Skip extra humidities
        record_bitstream.read(56)

        rain_rate = record_bitstream.read(16).uintle

        # ultraviolet_index
        record_bitstream.read(8)

        # solar_radiation
        record_bitstream.read(16)

        # storm_rain
        record_bitstream.read(16)

        # start_date_of_storm
        record_bitstream.read(16)

        # day_rain
        record_bitstream.read(16)

        # month_rain
        record_bitstream.read(16)

        # year_rain
        record_bitstream.read(16)

        # day_et
        record_bitstream.read(16)

        # month_et
        record_bitstream.read(16)

        # year_et
        record_bitstream.read(16)

        # Skip extra soil moistures
        record_bitstream.read(32)
        # Skip extra leaf wetnesses
        record_bitstream.read(32)

        # inside_alarms
        record_bitstream.read(8)

        # rain_alarms
        record_bitstream.read(8)

        # outside_alarms
        record_bitstream.read(16)

        # Skip extra temp/humidity alarms
        record_bitstream.read(64)
        # Skip extra soil leaf alarms
        record_bitstream.read(32)

        # Skip tx battery status
        record_bitstream.read(8)

        console_battery_voltage = (((record_bitstream.read(16).uintle * 300.0) / 512.0) / 100.0)
        forecast_icons = record_bitstream.read(8).uintle
        forecast_rule_number = record_bitstream.read(8).uintle
        sunrise = make_time(record_bitstream.read(16).uintle)
        sunset = make_time(record_bitstream.read(16).uintle)

        return cls(
            bar_trend=bar_trend,
            barometer=barometer,
            inside_temperature=inside_temperature,
            inside_humidity=inside_humidity,
            outside_temperature=outside_temperature,
            outside_humidity=outside_humidity,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            ten_min_avg_wind_speed=ten_min_avg_wind_speed,
            rain_rate=rain_rate,
            console_battery_voltage=console_battery_voltage,
            forecast_icons=forecast_icons,
            forecast_rule_number=forecast_rule_number,
            sunrise=sunrise,
            sunset=sunset,
            identifier=identifier,
            observation_made_at=observation_made_at)
