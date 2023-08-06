"""
Gets highway signs.
"""
# Standard Library
import functools
import io
import logging
from pathlib import Path
import shutil
from typing import Dict, IO, List, Optional
from urllib.parse import urlunparse

# Third Party Code
import requests

DMS_URL = "https://cotrip.org/device/getDMS.do"
IMAGE_HOST = "i.cotrip.org"

logger = logging.getLogger(__name__)


def get_all_signs() -> List[Dict]:
    """
    Gets all signs.
    """
    response = requests.get(DMS_URL)
    if response.status_code == requests.codes.ok:
        return response.json()["DMSDetails"]["DMS"]
    raise Exception("Couldn't fetch highway data.")


def get_sign_message(dms_id: str, signs: Optional[List[Dict]] = None) -> str:
    """
    Gets a particular sign's image url.
    """
    signs = signs or get_all_signs()
    for s in signs:
        if s["DMSId"] == dms_id:
            return urlunparse(
                ["https", IMAGE_HOST, s["MessageImage"], None, None, None]
            )
    raise ValueError("Could not find that sign.")


def fetch_sign_image(sign_id: str, all_signs: Optional[List[Dict]] = None) -> bytes:
    with requests.get(get_sign_message(sign_id, all_signs), stream=True) as r:
        if r.status_code == requests.codes.ok:
            r.raw.read = functools.partial(r.raw.read, decode_content=True)
            return r.content
    raise ValueError("Could not fetch sign.")


def store_sign_image(data: bytes, local_path: Path) -> None:
    with local_path.open("wb") as f:
        source: IO = io.BytesIO(data)
        dest: IO = f
        shutil.copyfileobj(source, dest)
