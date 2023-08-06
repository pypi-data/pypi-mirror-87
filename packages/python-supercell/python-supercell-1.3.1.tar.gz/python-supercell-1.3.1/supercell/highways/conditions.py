"""
Highway Conditions
"""
# Standard Library
from collections import defaultdict
import logging
from typing import Dict, List, Optional

# Third Party Code
import requests

SEGMENTS_URL = "https://cotrip.org/speed/getSegments.do"
CONDITIONS_URL = "https://cotrip.org/roadConditions/getRoadConditions.do"

logger = logging.getLogger(__name__)


def get_segments(
    road_name: str,
    start_mile_marker: float,
    end_mile_marker: float,
    direction: Optional[str] = None,
) -> Dict:
    """
    Gets segment conditions
    """
    logging.info(
        "Getting speed segments for %s %s between %s and %s",
        road_name,
        direction or "",
        start_mile_marker,
        end_mile_marker,
    )
    segments_response = requests.get(SEGMENTS_URL)
    segments = defaultdict(list)
    if segments_response.status_code == requests.codes.ok:
        for segment in segments_response.json()["SpeedDetails"]["Segment"]:
            if segment["RoadName"] == road_name:
                segment_start = float(segment["StartMileMarker"])
                segment_end = float(segment["EndMileMarker"])
                if start_mile_marker <= segment_start <= end_mile_marker or (
                    start_mile_marker < segment_end < end_mile_marker
                ):
                    d = {
                        "id": segment["SegmentId"],
                        "road_id": segment["RoadId"],
                        "name": segment["SegmentName"],
                        "direction": segment["Direction"],
                        "start": segment_start,
                        "end": segment_end,
                        "limit": int(segment["SpeedLimit"]),
                        "speed": int(segment["AverageSpeed"]),
                    }
                    if not direction or direction and d["direction"] == direction:
                        segments[d["direction"]].append(d)

    for key in segments.keys():
        if key == "N":
            segments[key].sort(key=lambda k: ["start"])
        else:
            segments[key].sort(key=lambda k: k["start"], reverse=True)
    return dict(segments)


def get_conditions(
    road_name: str, start_mile_marker: float, end_mile_marker: float
) -> List[Dict]:
    """
    Gets the road condtions.
    """
    logging.info(
        "Getting road conditions for %s from %s to %s",
        road_name,
        start_mile_marker,
        end_mile_marker,
    )
    conditions_response = requests.get(CONDITIONS_URL)
    conditions = []
    if conditions_response.status_code == requests.codes.ok:
        for condition in conditions_response.json()["RoadConditionsDetails"][
            "WeatherRoute"
        ]:
            if condition["RoadName"] == road_name:
                # if start_mile_marker <= float(condition["StartMileMarker"]) <= end_mile_marker:
                if start_mile_marker <= float(
                    condition["EndMileMarker"]
                ) and end_mile_marker >= float(condition["StartMileMarker"]):
                    d = {
                        "id": condition["WeatherRouteId"],
                        "road_id": condition["RoadId"],
                        "name": condition["RouteName"],
                        "start": float(condition["StartMileMarker"]),
                        "end": float(condition["EndMileMarker"]),
                        "conditions": condition["RoadCondition"],
                        "is_dangerous": condition["IsHazardousCondition"] == "true"
                        or False,
                    }
                    conditions.append(d)
    return conditions


def get_road_status(
    road_name: str,
    start_mile_marker: float,
    end_mile_marker: float,
    direction: Optional[str],
) -> Dict:
    """
    Retrieves road quality and conditions
    """
    logger.info(
        "Getting road status for %s %s between %s and %s",
        road_name,
        direction or "",
        start_mile_marker,
        end_mile_marker,
    )
    directions = get_segments(
        road_name=road_name,
        start_mile_marker=start_mile_marker,
        end_mile_marker=end_mile_marker,
        direction=direction,
    )
    conditions = get_conditions(
        road_name=road_name,
        start_mile_marker=start_mile_marker,
        end_mile_marker=end_mile_marker,
    )
    for key, items in directions.items():
        for item in items:
            for condition in conditions:
                if (
                    condition["start"] <= item["end"]
                    and condition["end"] >= item["start"]
                ):
                    item["conditions"] = condition["conditions"]
                    item["is_dangerous"] = condition["is_dangerous"]
    return directions
