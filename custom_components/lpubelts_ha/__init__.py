"""LPUBelts HA integration."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "lpubelts_ha"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the LPUBelts HA integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up LPUBelts from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = config_entry.data

    await hass.config_entries.async_forward_entry_setups(config_entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(config_entry, ["sensor"])
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True