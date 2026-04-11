import requests
import logging
from homeassistant.components.select import SelectEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CLOUD_URL = "https://appin.divoom-gz.com/Channel/MyClockGetList"

#INFO: https://docin.divoom-gz.com/web/#/5/360
async def async_setup_entry(hass, entry, async_add_entities):
    device_id = entry.data.get("device_id")
    clocks = {}
    
    try:
        params = {
            "DeviceId": device_id,
            "StartNum": 1,
            "EndNum": 100,
            "DeviceType": "Frame"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        response = await hass.async_add_executor_job(
            lambda: requests.get(CLOUD_URL, params=params, headers=headers, timeout=15)
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ReturnCode") == 0:
                clock_list = data.get("ClockList", [])
                for item in clock_list:
                    # Берем ClockName для списка и сохраняем соответствующий ClockId
                    name = item.get("ClockName")
                    clock_id = item.get("ClockId")
                    if name and clock_id:
                        clocks[name] = clock_id
                
                _LOGGER.info(f"Divoom: Good load: {len(clocks)} count in cloud")
            else:
                _LOGGER.error(f"Divoom Cloud API error: {data.get('ReturnMessage')}")
        else:
            _LOGGER.error(f"Divoom Cloud HTTP error: {response.status_code}")

    except Exception as e:
        _LOGGER.error(f"Failed to fetch clock list: {e}")

    # Если вдруг облако не ответило, создаем базовый вариант (заглушка)
    if not clocks:
        clocks = {"Default Face": 1}

    async_add_entities([DivoomClockSelect(hass, entry, clocks)], True)

class DivoomClockSelect(SelectEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "divoom_clock"
    _attr_icon = "mdi:clock-outline"

    def __init__(self, hass, entry, clocks):
        self._hass = hass
        self._entry = entry
        self._clocks = clocks
        self._url = f"http://{entry.data['host']}:{entry.data['port']}/divoom_api"
        
        self._attr_unique_id = f"{entry.entry_id}_clock_select"
        self._attr_options = list(clocks.keys())
        
        # Восстановление состояния
        saved_option = hass.data[DOMAIN].get(f"{entry.entry_id}_clock")
        if saved_option in self._attr_options:
            self._attr_current_option = saved_option
        else:
            self._attr_current_option = self._attr_options[0] if self._attr_options else None
    
    #INFO: https://docin.divoom-gz.com/web/#/5/361
    async def async_select_option(self, option: str) -> None:
        clock_id = self._clocks.get(option)
        if clock_id is None:
            return
        
        payload = {
            "Command": "Channel/SetClockSelectId",
            "ClockId": int(clock_id)
        }
        try:
            response = await self._hass.async_add_executor_job(
                lambda: requests.get(self._url, json=payload, timeout=5)
            )
            response.raise_for_status()
            self._attr_current_option = option
            self._hass.data[DOMAIN][f"{self._entry.entry_id}_clock"] = option
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(f"Error setting clock to {option} (ID: {clock_id}): {e}")
