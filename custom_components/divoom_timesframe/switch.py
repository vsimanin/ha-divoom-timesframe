import requests
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DivoomScreenSwitch(data["coordinator"], entry, data["url"])], True)

class DivoomScreenSwitch(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, entry, url):
        super().__init__(coordinator)
        self._url = url
        self._attr_unique_id = f"{entry.entry_id}_screen"
        self._attr_translation_key = "divoom_screen"
        self._attr_has_entity_name = True

    @property
    def is_on(self):
        return self.coordinator.data.get("OnOff") == 1

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(
            lambda: requests.get(self._url, json={"Command": "Channel/OnOffScreen", "OnOff": 1}, timeout=5)
        )

        self.coordinator.data["OnOff"] = 1
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(
            lambda: requests.get(self._url, json={"Command": "Channel/OnOffScreen", "OnOff": 0}, timeout=5)
        )
        self.coordinator.data["OnOff"] = 0
        self.async_write_ha_state()
        
