import logging
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

DOMAIN = "lpubelts_ha"

SCAN_INTERVAL = timedelta(hours=1)

LEADERBOARD_URL = "https://explore.lpubelts.com/data/leaderboardData.json"

METRICS = [
    "display_name",
    "dan_level",
    "dan_points",
    "black_belt_count",
    "black_belt_awarded_at_date",
    "diagnostics_api_connected",
    "diagnostics_last_updated",
]

ICON_MAP = {
    "display_name": "mdi:account",
    "dan_level": "mdi:trophy",
    "dan_points": "mdi:star-outline",
    "black_belt_count": "mdi:lock-open-variant",
    "black_belt_awarded_at_date": "mdi:calendar",
    "diagnostics_api_connected": "mdi:calendar",
    "diagnostics_last_updated": "mdi:clock-outline",
}

FRIENDLY_NAMES = {
    "display_name": "Display name",
    "dan_level": "Dan level",
    "dan_points": "Dan points",
    "black_belt_count": "Black belt count",
    "black_belt_awarded_at_date": "Black belt awarded at",
    "diagnostics_api_connected": "API",
    "diagnostics_last_updated": "Last Updated",
}

__all__ = [
    "_LOGGER",
    "DOMAIN",
    "SCAN_INTERVAL",
    "LEADERBOARD_URL",
    "METRICS",
    "ICON_MAP",
    "FRIENDLY_NAMES",
]