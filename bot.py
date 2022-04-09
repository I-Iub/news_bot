import os
import time

import requests
from telegram import Bot
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DELAY = 60 * 20  # периодичность опроса, секунд
# словарь с ингредиентами для bs4 для разных сайтов
SITES = {
    'vc.ru': {
        'url': 'https://vc.ru/',
        'ingredients': {
            'name': 'a',
            'class': 'content-link',
            'limit': 1
        }
    },
}

bot = Bot(token=TELEGRAM_TOKEN)


def send_message(message):
    """Телаграм-бот отправляет сообщение в чат."""
    bot.send_message(CHAT_ID, message)


def get_html(url):
    """Делает запрос по url и возвращает html-код страницы"""
    try:
        response = requests.get(url)
        return response.text  # HTML-код
    except Exception as error:
        send_message(f'При запросе к {url} возникла ошибка:\n{error}')


def get_news(html, **kwargs):
    """Извлекает из html-кода ссылку на последнюю
    статью и возвращяет её в виде строки.
    """
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all(**kwargs)
    return news[0].get('href')


def main():
    send_message('Программа слежения за новостями запущена.')
    last_news = {site_name: None for site_name, _ in SITES.items()}  # кэш
    while True:
        for site_name, data in SITES.items():
            html = get_html(data.get('url'))
            if html is None:
                continue

            news = get_news(html, **data['ingredients'])
            # проверка является ли полученная ссылка на статью новой
            if news is None or news == last_news.get(site_name):
                continue
            # если получена новая ссылка на статью, кэшируем и отправляем в чат
            last_news[site_name] = news
            send_message(f'{site_name}:\n{news}')
        time.sleep(DELAY)  # задержка перед следующим опросом


if __name__ == '__main__':
    main()
