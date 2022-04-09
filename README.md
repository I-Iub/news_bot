### Запуск программы
Распакуйте архив или клонируйте проект с github по ссылке [https://github.com/I-Iub/news_bot](https://github.com/I-Iub/news_bot).

Перейдите в папку с проектом и создайте файл .env. В файле укажите токен Телеграм-бота и id чата Телеграм, в который будут отправляться сообщения.
```
TELEGRAM_TOKEN = <token>
TELEGRAM_CHAT_ID = <id>
```

Создайте и активируйте виртуальное окружение, установите зависимости. Например, в случае venv:
```
python -m venv venv
source venv/bin/activate        # Linux
source venv/Scripts/activate    # Windows
pip install -r requirements.txt
```
Запустите программу из командной строки:
```
python bot.py
```
