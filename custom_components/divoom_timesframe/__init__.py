import logging
import requests
import json
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Инициализируем хранилище данных, если его нет
    hass.data.setdefault(DOMAIN, {})
    # Сохраняем конфиг текущего устройства
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Регистрация службы для отправки текста
    async def async_handle_send_text(call):
        host = entry.data.get("host")
        port = entry.data.get("port")
        url = f"http://{host}:{port}/divoom_api"
        
        # Забираем все данные из вызова
        message = call.data.get("message", "Hello!")
        color_raw = call.data.get("color", "#FFFFFF")
        x = call.data.get("x", 0)
        y = call.data.get("y", 16)
        
        # Конвертируем цвет из палитры [R,G,B] в HEX #RRGGBB
        if isinstance(color_raw, list):
            color = "#%02x%02x%02x" % tuple(color_raw)
        else:
            color = color_raw

        # 3. Формируем запрос к рамке
        payload = {
            "Command": "Draw/SendHttpText",
            "TextId": 1,
            "x": x,
            "y": y,
            "dir": 0,
            "font": 2,
            "TextWidth": 128,
            "speed": 100,
            "TextString": message,
            "color": color,
            "align": 2
        }

        try:
            # Используем POST для стабильности (но нужно проверять, не тестил!!!)
            response = await hass.async_add_executor_job(
                lambda: requests.post(url, json=payload, timeout=5)
            )
            response.raise_for_status()
        except Exception as e:
            _LOGGER.error(f"Error sending text to Divoom: {e}")

    # Регистрируем службу в Home Assistant
    hass.services.async_register(DOMAIN, "send_text", async_handle_send_text)

    # Запускаем платформы switch, number и select
    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "number", "select"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["switch", "number", "select"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
