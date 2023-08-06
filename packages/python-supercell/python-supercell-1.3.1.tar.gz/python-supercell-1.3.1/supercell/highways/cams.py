"""
Highway Cameras
"""
# Standard Library
import functools
import io
import logging
from pathlib import Path
import shutil
from typing import IO, Tuple
from urllib.parse import urlunparse

# Third Party Code
import requests

HOST = "i.cotrip.org"
PATH = "/dimages/camera"
QUERY_PARAM = "imageURL"

logger = logging.getLogger(__name__)


def fetch_cam(cam: str) -> Tuple[str, bytes]:
    """
    Fetches an frame from a camera.
    """
    name, cam_path = cam.split(":")
    logger.info("Downloading Camera %s to %s", cam_path, name)
    image_url = urlunparse(
        ["https", HOST, PATH, None, "%s=%s" % (QUERY_PARAM, cam_path), None]
    )
    with requests.get(image_url, stream=True) as r:
        if r.status_code == requests.codes.ok:
            r.raw.read = functools.partial(r.raw.read, decode_content=True)
            return name, r.content
    raise ValueError("Could not fetch that camera.")


def store_cam(name: str, data: bytes, directory: str) -> Path:
    """
    Stores data to a local file.
    """
    local_path = Path(directory, "highway-cam-%s.jpg" % name)
    with open(local_path, "wb") as f:
        source: IO = io.BytesIO(data)
        dest: IO = f
        shutil.copyfileobj(source, dest)
    return local_path


def download_cam(cam: str, directory: str) -> str:
    """
    Fetches and then stores a camera image.
    """
    name, data = fetch_cam(cam)
    return str(store_cam(name, data, directory).resolve())
