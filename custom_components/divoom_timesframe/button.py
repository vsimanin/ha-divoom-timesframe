import requests
import logging
from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([DivoomRebootButton(hass, entry)], True)

class DivoomRebootButton(ButtonEntity):
    _attr_has_entity_name = True
    _attr_device_class = "restart"
    _attr_translation_key = "divoom_reboot"

    def __init__(self, hass, entry):
        self._hass = hass
        self._url = f"http://{entry.data['host']}:{entry.data['port']}/divoom_api"
        self._attr_unique_id = f"{entry.entry_id}_reboot"

    async def async_press(self) -> None:
        payload = {"Command": "Device/SysReboot"}
        try:
            response = await self._hass.async_add_executor_job(
                lambda: requests.get(self._url, json=payload, timeout=5)
            )
            response.raise_for_status()
        except Exception as e:
            _LOGGER.error(f"Error rebooting Divoom device: {e}")
