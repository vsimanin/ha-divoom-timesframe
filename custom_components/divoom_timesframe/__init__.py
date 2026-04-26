import logging
from datetime import timedelta
import requests
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data.get("host")
    port = entry.data.get("port")
    device_id = entry.data.get("device_id")
    url = f"http://{host}:{port}/divoom_api"

    async def async_update_data():
        try:
            response = await hass.async_add_executor_job(
                lambda: requests.get(url, json={"Command": "Channel/GetOnOffScreen"}, timeout=5)
            )
            response.raise_for_status()
            return response.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="divoom_timesframe_status",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "url": url
    }

    async def async_handle_send_danmaku(call):
        message = call.data.get("message", "")[:100] # Ограничение 100 символов
        color_raw = call.data.get("color", "#FFFFFF")

        color = "#%02x%02x%02x" % tuple(color_raw) if isinstance(color_raw, list) else color_raw

        payload = {
            "Command": "Danmaku/SendText",
            "DeviceId": int(device_id),
            "Text": message,
            "TextColor": color,
            "UserId": 1
        }

        try:
            response = await hass.async_add_executor_job(
                lambda: requests.post(url, json=payload, timeout=5)
            )
            response.raise_for_status()
        except Exception as e:
            _LOGGER.error(f"Error sending Danmaku to Divoom: {e}")

    hass.services.async_register(DOMAIN, "send_danmaku", async_handle_send_danmaku)

    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "number", "select", "button"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["switch", "number", "select", "button"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok