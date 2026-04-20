# Divoom TimesFrame Integration for Home Assistant
🇷🇺 **Divoom TimesFrame** — это пользовательская интеграция для Home Assistant, которая позволяет управлять панелями Divoom TimesFrame через локальный HTTP API.  
На данный момент продукт находится на этапе предрелиза. Пожалуйста, присоединяйтесь к разработке, если у вас есть желание улучшить функционал интеграции!  

**API DOC**: https://docin.divoom-gz.com/web/#/5/25  

## Функционал

- 📺 **Управление экраном**: Включение и выключение дисплея
- ☀️ **Яркость**: Плавная регулировка яркости (0-100%)
- 🕒 **Выбор оболочек**: Удобный список со всеми вашими оболочками, загруженными из облака Divoom
- 🔄 **Перезагрузка**: Кнопка для удаленной перезагрузки устройства
- ⚡ **Локальное управление**: Команды отправляются напрямую на устройство по локальной сети через GET-запросы 
- 👁️ **Опрос состояния экрана**: получение реального состояния экрана раз в 30 секунд


## Установка   
1. Откройте HACS в Home Assistant  
2. Добавьте ссылку на этот репозиторий и выберите Divoom TimesFrame
3. Нажмите "Скачать"
4. Добавьте интеграцию Divoom TimesFrame в меню Устройства и службы
5. Введите IP, порт и DeviceID (узнать можно тут: https://app.divoom-gz.com/Device/ReturnSameLANDevice)

---

🇺🇸 **Divoom TimesFrame** is a custom integration for Home Assistant that allows you to control Divoom TimesFrame panels via a local HTTP API.  
This product is currently in the pre-release stage. Please feel free to join the development if you'd like to help improve the integration!  

**API DOC**: https://docin.divoom-gz.com/web/#/5/25 

## Features

- 📺 Screen Control: Turn the display on and off  
- ☀️ Brightness: Smooth brightness adjustment (0-100%)  
- 🕒 Watchface Selection: A convenient list of all your watchfaces synced from the Divoom cloud  
- 🔄 Restart: A button for remote device reboot  
- ⚡ Local Control: Commands are sent directly to the device over the local network via GET requests 
- 👁️ **Screen state poll**: get the real state of the screen every 30 seconds. 

## Installation

1. Open HACS in Home Assistant
2. Add this repository URL as a Custom Repository and select Divoom TimesFrame
3. Click Download
4. Go to Settings > Devices & Services and add the Divoom TimesFrame integration
5. Enter the IP address, Port, and DeviceID (you can find it here: https://app.divoom-gz.com/Device/ReturnSameLANDevice)  
