import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
import time
import random

def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file]
    return links

def get_page_data(link, retries=3):
    """Получение данных с одной страницы с повторными попытками"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    for attempt in range(retries):
        try:
            response = requests.get(link, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Получение заголовка
                title_tag = soup.find('h1', {'data-marker': 'item-view/title-info'})
                title = title_tag.text.strip() if title_tag else "N/A"
                
                # Получение цены
                price_tag = soup.find('span', {'data-marker': 'item-view/item-price'})
                price = price_tag.text.strip() if price_tag else "N/A"
                
                # Получение количества просмотров
                views_tag = soup.find('span', {'data-marker': 'item-view/total-views'})
                views = views_tag.text.strip() if views_tag else "N/A"
                
                return {'Link': link, 'Title': title, 'Price': price, 'Views': views}
            else:
                logger.error(f"Ошибка: Не удалось получить доступ к странице {link}, статус-код: {response.status_code}")
                if response.status_code == 429:
                    logger.info("Достигнут лимит запросов. Ждем 60 секунд перед следующей попыткой.")
                    time.sleep(60)  # Ждем 60 секунд перед следующей попыткой
        except requests.RequestException as e:
            logger.error(f"Ошибка: Не удалось получить доступ к странице {link}. Попытка {attempt + 1} из {retries}. Ошибка: {e}")
        time.sleep(random.uniform(10, 20))  # Увеличенная задержка между повторными попытками
    return None

def collect_data(links, delay):
    data = []
    for link in links:
        page_data = get_page_data(link)
        if page_data:
            data.append(page_data)
            logger.info(f"Обработана ссылка {link}, задержка {delay} секунд перед следующей ссылкой.")
        time.sleep(random.uniform(delay, delay + 15))  # Еще более случайная задержка перед запросом следующей ссылки
    return data

def save_data_to_excel(data, file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    logger.info(f"Сохранено {len(data)} записей в файл {file_name}")

if __name__ == "__main__":
    file_path = r'C:\Install\chromedriver\avito_links.txt'
    output_file = 'avito_data.xlsx'
    delay = 15.0  # Увеличенная задержка в секундах
    
    links = read_links_from_file(file_path)
    data = collect_data(links, delay)
    save_data_to_excel(data, output_file)
