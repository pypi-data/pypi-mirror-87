"""Fetches GOES images from NOAA."""
# Standard Library
from datetime import date, datetime
import os
from pathlib import Path
import re
from typing import Dict, List, Union
from urllib.parse import urljoin, urlunparse

# Third Party Code
import requests

IMAGE_HOST = "cdn.star.nesdis.noaa.gov"

IMAGE_PATTERN = r"https://{host}(?P<image_path>[" r"a-zA-Z0-9/:\-_.]+)',\s+".format(
    host=re.escape(IMAGE_HOST)
)
IMAGE_COMPPAT = re.compile(IMAGE_PATTERN)

FILE_PATTERN = (
    r"/GOES(?P<sat_num>\d{2})"
    r"/ABI/SECTOR/"
    r"(?P<sector>[a-z]{2,3})/(?P<band>[A-Za-z]+)/"
    r"(?P<t_year>\d{4})"
    r"(?P<t_daynum>\d{3})"
    r"(?P<t_hour>\d{2})"
    r"(?P<t_minute>\d{2})"
    r"_GOES\d{2}-ABI-"
    r"[a-z]{2,3}-[A-Za-z]+-(?P<i_width>\d+)x(?P<i_height>\d+).jpg"
)

IMAGE_COMPOSE = (
    "/GOES{sat_num}/ABI/SECTOR/{sector}/{band}/{t_year}"
    "{t_daynum}{t_hour}{t_minute}_GOES{sat_num}-ABI-{sector}"
    "-{band}-{i_width}x{i_height}.jpg"
)

FILE_COMPPAT = re.compile(FILE_PATTERN)

SATS = {
    "WEST": {"id": "G17", "sectors": {"Pacific Coast": "wus"},},
    "EAST": {
        "id": "G16",
        "sectors": {
            "Northern Rockies": "nr",
            "Upper Mississippi Valley": "umv",
            "Great Lakes": "cgl",
        },
    },
}

GEOCOLOR_BAND = "GEOCOLOR"
SANDWICH_BAND = "Sandwich"

BANDS = {
    GEOCOLOR_BAND,
    SANDWICH_BAND,
}

LENGTHS = {12, 24, 36, 48, 60, 72, 84, 96}


def get_image_data(image_url: str) -> Dict:
    """Produces image data from a URL"""
    mappings = [
        ("t_year", int),
        ("t_daynum", int),
        ("t_hour", str),
        ("t_minute", str),
        ("i_width", int),
        ("i_height", int),
        ("sat_num", int),
        ("sector", str),
        ("band", str),
    ]
    data = FILE_COMPPAT.search(image_url)
    ret = {}
    if data:
        for k, f in mappings:
            match = data.group(k)
            ret[k] = f(match)
    return ret


def does_exist(url: str) -> bool:
    """Determines if a particular file exists on the server."""
    resp = requests.head(url)
    if resp.status_code == requests.codes.ok:
        return True
    return False


def image_url_from_data(image_data: Dict) -> str:
    """Produces a URL from a dictionary of parameters"""
    image_path = IMAGE_COMPOSE.format(
        sat_num=image_data["sat_num"],
        sector=image_data["sector"],
        band=image_data["band"],
        t_year=image_data["t_year"],
        t_daynum=image_data["t_daynum"],
        t_hour=image_data["t_hour"],
        t_minute=image_data["t_minute"],
        i_width=image_data["i_width"],
        i_height=image_data["i_height"],
    )
    return urlunparse(["https", IMAGE_HOST, image_path, None, None, None])


def in_cache(key: str, directory: str) -> Path:
    """Determines if we already have downloaded an image."""
    full_key = Path(directory, key)
    if os.path.exists(full_key):
        return full_key
    raise ValueError("Not in cache.")


def store_in_cache(key: str, data: bytes, directory: str) -> Path:
    """
    Stores some data in a file in a directory.
    """
    full_key = Path(directory, key)
    with open(full_key, "wb") as fh:
        fh.write(data)
    return full_key


def full_day_images(
    sat: str,
    sector: str,
    band: str,
    size: int = 600,
    anchor_datetime: Union[datetime, None] = None,
) -> List:
    """Produces urls for a full day"""
    now = anchor_datetime or datetime.utcnow()
    day_num = int(now.strftime("%j"))
    now_time = int(now.strftime("%H%M"))
    year = now.year
    sat_num = sat[1:]

    def make_url(path: str) -> str:
        """Produces a full URL from a path"""
        return urlunparse(["https", IMAGE_HOST, path, None, None, None])

    index_path = "/GOES{sat_num}/ABI/SECTOR/{sector}/{band}/".format(
        sat_num=sat_num, sector=sector, band=band
    )

    if day_num == 1:  # First day of the new year
        year_two = year - 1
        prev_day_num = (date(year + 1, 1, 1) - date(year, 1, 1)).days
    else:
        year_two = year
        prev_day_num = day_num - 1

    # A pattern which will match all the images corresponding to a specific date.
    pattern_string = (
        r"(?P<file_name>(?P<year>{yearone}|{yeartwo})(?P<day_num>{day_num}|{prev_day_num})(?P<time>["
        r"0-9]{{4}})_GOES{sat_num}-ABI-{sector}-{band}-{size}x{size}.jpg)"
    )
    pattern = re.compile(
        pattern_string.format(
            yearone=year,
            yeartwo=year_two,
            day_num=day_num,
            prev_day_num=prev_day_num,
            sat_num=sat_num,
            sector=sector,
            band=band,
            size=size,
        )
    )
    # Get a list of every image available on the NOAA servers (in HTML)
    index_response = requests.get(make_url(index_path))

    if index_response.status_code == requests.codes.ok:
        # Produce a list of matching image urls for the day and time we care about.
        matches = {
            make_url(urljoin(index_path, i_filename))
            for i_filename, _, i_daynum, i_time in pattern.findall(index_response.text)
            if int(i_daynum) == day_num
            or (int(i_daynum) == prev_day_num and int(i_time) > now_time)
        }
        return sorted(list(matches))
    else:
        return []
