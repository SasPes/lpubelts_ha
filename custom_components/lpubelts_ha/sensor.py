from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import _LOGGER, DOMAIN, METRICS, ICON_MAP
from .helpers import friendly_metric_name, humanize_since, parse_timestamp
from .coordinator import LPUBeltsDataCoordinator

async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.debug("Setting up LPUBelts sensors")
    coordinator = LPUBeltsDataCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    display_name = config_entry.data.get("display_name")
    if not display_name:
        _LOGGER.error("Missing 'display_name' in config entry")
        return

    entities = [LPUBeltsMetricSensor(coordinator, display_name, key) for key in METRICS]
    async_add_entities(entities, True)

class LPUBeltsMetricSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, display_name: str, metric_key: str):
        super().__init__(coordinator)
        self._display_name = display_name
        self._metric_key = metric_key

        self._attr_has_entity_name = True
        self._attr_name = friendly_metric_name(metric_key)
        self._attr_unique_id = f"lpubelts_{display_name}_{metric_key}"
        self._attr_icon = ICON_MAP.get(metric_key)

        if metric_key in ("diagnostics_api_connected", "diagnostics_last_updated"):
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def icon(self):
        if self._metric_key == "diagnostics_api_connected":
            return "mdi:check-network-outline" if self.coordinator.last_update_success else "mdi:close-network-outline"
        return self._attr_icon

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"user_{self._display_name}")},
            "name": self._display_name,
            "manufacturer": "SasPes via LPUBelts",
            "model": "Leaderboard ➜ Black Belts",
            "sw_version": "1.0",
        }

    @property
    def available(self):
        return self.coordinator.last_update_success

    def _user_data(self):
        data = self.coordinator.data or {}
        users = data.get("data", [])
        target = (self._display_name or "").strip().casefold()
        return next(
            (u for u in users if (u.get("displayName") or "").strip().casefold() == target),
            None,
        )

    @property
    def native_value(self):
        if self._metric_key == "diagnostics_api_connected":
            return "Connected" if self.coordinator.last_update_success else "Disconnected"

        if self._metric_key == "diagnostics_last_updated":
            return humanize_since(getattr(self.coordinator, "last_success_at", None)) or "N/A"

        user = self._user_data()
        if not user:
            return None

        if self._metric_key == "black_belt_awarded_at_date":
            dt = parse_timestamp(user.get("blackBeltAwardedAt"))
            return f"{dt.strftime('%B')} {dt.day}, {dt.year}" if dt else None

        mapping = {
            "display_name": user.get("displayName"),
            "dan_level": user.get("danLevel"),
            "dan_points": user.get("danPoints"),
            "black_belt_count": user.get("blackBeltCount"),
        }
        return mapping.get(self._metric_key)

    @property
    def extra_state_attributes(self):
        if self._metric_key in ("diagnostics_api_connected", "diagnostics_last_updated"):
            return {}

        user = self._user_data()
        if not user:
            return {}

        dt = parse_timestamp(user.get("blackBeltAwardedAt"))
        attrs_raw = {
            "display_name": user.get("displayName"),
            "dan_level": user.get("danLevel"),
            "dan_points": user.get("danPoints"),
            "black_belt_count": user.get("blackBeltCount"),
            "black_belt_awarded_at_date": f"{dt.strftime('%B')} {dt.day}, {dt.year}" if dt else None,
        }
        return {friendly_metric_name(k): v for k, v in attrs_raw.items()}