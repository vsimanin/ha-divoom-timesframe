import requests
import logging
from homeassistant.components.number import NumberEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([DivoomBrightness(hass, entry)], True)

class DivoomBrightness(NumberEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "divoom_brightness"
    _attr_icon = "mdi:brightness-6"

    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry
        self._url = f"http://{entry.data['host']}:{entry.data['port']}/divoom_api"
        self._attr_unique_id = f"{entry.entry_id}_brightness"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._state = hass.data[DOMAIN].get(f"{entry.entry_id}_bright", 100)

    @property
    def native_value(self):
        return self._state

    async def async_set_native_value(self, value: float) -> None:
        val = int(value)
        payload = {"Command": "Channel/SetBrightness", "Brightness": val}

        try:
            response = await self._hass.async_add_executor_job(
                lambda: requests.get(self._url, json=payload, timeout=5)
            )
            response.raise_for_status()
            self._state = val
            self._hass.data[DOMAIN][f"{self._entry.entry_id}_bright"] = val
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error("Ошибка при установке яркости Divoom: %s", e)

    @property
    def available(self) -> bool:
        return True
