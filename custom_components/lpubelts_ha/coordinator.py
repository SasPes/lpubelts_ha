import asyncio
from datetime import datetime, timezone

import aiohttp
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import _LOGGER, SCAN_INTERVAL, LEADERBOARD_URL

BLACKLISTED_USER_IDS = {
    "CluvPi5PCAckLJhl5M4rynUmslb2",
}

class LPUBeltsDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(hass, _LOGGER, name="LPUBelts", update_interval=SCAN_INTERVAL)
        self.last_success_at: datetime | None = None
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self):
        try:
            _LOGGER.debug("Fetching data from %s", LEADERBOARD_URL)
            async with async_timeout.timeout(10):
                async with self._session.get(LEADERBOARD_URL) as response:
                    status = response.status
                    _LOGGER.debug("API response status: %s", status)
                    if status != 200:
                        raise UpdateFailed(f"Error fetching data: {status}")

                    try:
                        data = await response.json()
                    except aiohttp.ContentTypeError as err:
                        text = await response.text()
                        _LOGGER.error("Invalid JSON content: %s", text[:200])
                        raise UpdateFailed("Invalid JSON content from API") from err

                    users = data.get("data")
                    if users is None or not isinstance(users, list):
                        _LOGGER.warning("Unexpected payload format: %s", list(data.keys()))
                        data = {"data": []}
                    else:
                        # Filter out blacklisted users and users without danPoints
                        filtered_users = [
                            u for u in users
                            if u.get("danPoints") and u.get("id") not in BLACKLISTED_USER_IDS
                        ]
                        sorted_users = sorted(filtered_users, key=lambda u: u.get("danPoints", 0), reverse=True)

                        for idx, user in enumerate(sorted_users, start=1):
                            user["position"] = idx

                        data["data"] = sorted_users

                    _LOGGER.debug("Fetched data for %d users", len(data.get("data", [])))
                    self.last_success_at = datetime.now(timezone.utc)
                    return data

        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout while fetching data from API")
            raise UpdateFailed("Timeout while fetching data from API") from err
        except aiohttp.ClientError as err:
            _LOGGER.error("Client error communicating with API: %s", err)
            raise UpdateFailed(f"Client error communicating with API: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error communicating with API: %s", err, exc_info=True)
            raise UpdateFailed(f"Error communicating with API: {err}") from err