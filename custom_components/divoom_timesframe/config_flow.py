import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class DivoomFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"TimesFrame ({user_input['host']})",
                data=user_input
            )
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Optional("port", default=9000): int,
                vol.Required("device_id"): int, 
            })
        )
