from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol

class LPUBeltsConfigFlow(config_entries.ConfigFlow, domain="lpubelts_ha"):
    """Handle a config flow for LPUBelts."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            display_name = user_input["display_name"]
            await self.async_set_unique_id(display_name)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=display_name,
                data={"display_name": display_name},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("display_name"): vol.Coerce(str),
            }),
        )