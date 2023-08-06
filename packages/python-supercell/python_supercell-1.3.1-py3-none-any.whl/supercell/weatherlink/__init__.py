"""
Tools for retrieving the current conditions from a Davis Weatherlink IP Logger
"""
# Standard Library
import logging
import socket
import time

# Supercell Code
from supercell.weatherlink.exceptions import BadCRC, NotAcknowledged, UnknownResponseCode
from supercell.weatherlink.models import StationObservation
from supercell.weatherlink.utils import connect, receive_data, request

LOOP_COMMAND = b"LOOP %d\n"
LOOP_RECORD_SIZE_BYTES = 99
LOOP_RECORD_SIZE_BITS = LOOP_RECORD_SIZE_BYTES * 8


logger = logging.getLogger(__name__)


def get_current(host: str, port: int) -> bytes:
    """Gets the current readings on the device."""
    sock = connect(host, port)
    loop_data = b""
    try:
        try:
            request(sock, LOOP_COMMAND % 1)
        except (BadCRC, NotAcknowledged, UnknownResponseCode):
            logger.exception("Could not issue loop command.")
            raise

        while len(loop_data) != LOOP_RECORD_SIZE_BYTES:
            data = receive_data(sock)
            loop_data += data
    except socket.timeout:
        logger.exception("Could not issue loop command")
        raise NotAcknowledged()
    finally:
        sock.close()
    return loop_data


def get_current_condition(host: str, port: int) -> StationObservation:
    """Obtains the current conditions."""
    try:
        current_bytes = get_current(host, port)
    except (BadCRC, NotAcknowledged, UnknownResponseCode):
        # Wait a little and try again.
        time.sleep(0.1)
        try:
            current_bytes = get_current(host, port)
        except (BadCRC, NotAcknowledged, UnknownResponseCode):
            # Wait twice as long and try again.
            time.sleep(1.0)
            try:
                current_bytes = get_current(host, port)
            except (BadCRC, NotAcknowledged, UnknownResponseCode):
                # Ok just give up.
                raise
    return StationObservation.init_with_bytes(current_bytes)
