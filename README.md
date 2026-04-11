# Divoom TimesFrame Integration for Home Assistant
🇷🇺 DivoomTimesFrame — это пользовательская интеграция для Home Assistant, которая позволяет управлять панелями Divoom TimesFrame через локальный HTTP API. Проект находится на стадии активной разработки!  

ВАЖНО! На данный момент продукт находится на этапе предрелиза. Сейчас нет возможности опрашивать состояние устройства, так как предоставленная документация не содержит нужной информации, а метод GetAllConf не возвращает статус, в отличие от других продуктов бренда. Я уже направил запрос разработчику и ожидаю обратной связи. Пожалуйста, присоединяйтесь к разработке!  

🇺🇸 DivoomTimesFrame is a custom Home Assistant integration for controlling Divoom TimesFrame displays via the local HTTP API. This project is currently in early development!  

IMPORTANT! This product is currently in the pre-release stage. At the moment, there is no way to poll the device status because the provided documentation lacks this information, and the GetAllConf method does not return the status (unlike other products from this brand). I have contacted the developer regarding this issue and am awaiting feedback. Contributions are welcome!  

API DOC: https://docin.divoom-gz.com/web/#/5/25  

🛠 Статус проекта / Project Status  
    Initial API implementation (based on Divoom Doc)  
    HACS compatibility  
    Basic sensors and services (service_text, brightness, screen_on/off, change_faceid)  

⚙️ Установка / Installation  
HACS (Manual)  
    1. Откройте HACS в Home Assistant.  
    2. Перейдите в Integrations -> Custom Repositories.  
    3. Добавьте ссылку на этот репозиторий и выберите Divoom TimesFrame.  
    4. Нажмите «Установить».  
    ---  
    1. Open HACS in Home Assistant.  
    2. Go to Integrations -> Custom Repositories.  
    3. Add this repository URL and select Divoom TimesFrame.  
    4. Click "Install".  

📖 Использование / Usage  
На данном этапе проект находится в зачаточном состоянии. Основная цель — реализовать полноценную отправку уведомлений и локальное управление через HA.  
The project is in its early stages. The main goal is to implement full notification support and frame management local directly through HA.  
