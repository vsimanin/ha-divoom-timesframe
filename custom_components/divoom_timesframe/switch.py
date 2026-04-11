import requests, json
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([DivoomScreenSwitch(hass, entry)], True)

#INFO: https://docin.divoom-gz.com/web/#/5/367
class DivoomScreenSwitch(SwitchEntity):
    def __init__(self, hass, entry):
        self._hass = hass
        self._entry = entry
        self._url = f"http://{entry.data['host']}:{entry.data['port']}/divoom_api"
        self._attr_unique_id = f"{entry.entry_id}_screen"
        self._attr_translation_key = "divoom_screen"
        self._attr_has_entity_name = True 
        # Состояние из памяти или ставим True
        self._state = hass.data[DOMAIN].get(f"{entry.entry_id}_state", True)

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        requests.post(self._url, json={"Command": "Channel/OnOffScreen", "OnOff": 1}, timeout=5)
        self._state = True
        self._hass.data[DOMAIN][f"{self._entry.entry_id}_state"] = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        requests.post(self._url, json={"Command": "Channel/OnOffScreen", "OnOff": 0}, timeout=5)
        self._state = False
        self._hass.data[DOMAIN][f"{self._entry.entry_id}_state"] = False
        self.schedule_update_ha_state()
