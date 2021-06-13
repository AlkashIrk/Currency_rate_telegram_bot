# Currency_rate_telegram_bot
## Описание
Бот предназначен для быстрой конвертации валюты, посредством мессенджера Telegram.

Используется курсы ЦБ РФ

Данные берутся с сайта [Курсы валют, API](https://www.cbr-xml-daily.ru/)

* RUB -> USD
* RUB -> EUR
* RUB -> GPB
* и еще около 30 валют...


В первый раз по умолчанию происходит конвертация RUB -> USD.

Для конвертации просто введите число в чат.

Изменить валюту можно в настройках.



Пример работы бота:
https://t.me/Curr_CBR_rate_bot

## Установка
##### Создание venv окружения
```
"%userprofile%\AppData\Local\Programs\Python\Python38\python.exe" -m venv venv 
venv\Scripts\pip install -r requirements.txt
```

##### Запуск бота
```
venv\Scripts\python.exe start_bot.py
```