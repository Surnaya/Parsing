# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и 
# извлечь информацию о всех книгах на сайте во всех категориях: 
# - название, 
# - цену, 
# - количество товара в наличии (In stock (19 available)) в формате integer, 
# - описание.

# Затем сохранить эту информацию в JSON-файле.

import json
from datetime import datetime, time, timedelta
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
url = 'http://books.toscrape.com'
url_1 = 'http://books.toscrape.com'


name =[]
price =[]
count = []
content =[]
output = {}


while True:

    response = requests.get(url, headers=headers)
    # Парсинг HTML-содержимого веб-страницы с помощью Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    next_page_link = soup.find('a', {'class': 'next'})
    results = soup.find('ol', {'class':'row'})
    # Вывод ссылок на
    release_links = []
    for i in results:
        for link in soup.find_all('div', ('class', "image_container")):
            atag=link.find('a')
            if atag:
                release_links.append(atag.get('href'))

    url_join = []
    url_join = [urllib.parse.urljoin('https://www.boxofficemojo.com', link) for link in release_links]

    for i in url_join:
        response = requests.get(i)
        soup = BeautifulSoup(response.content, 'html.parser')

    # Парсинг названия книги. Обработка исключения: добавляем пустую строку.
        try:
            name.append(soup.find('div', ('class', 'col-sm-6 product_main')).find('h1').text)
        except:
            name.append('')

    # Парсинг цены книги. 
        try:
            p = soup.find('p',('class','price_color')).text
            # p = float(re.sub(r'[^\d.]+', '', p))
            price.append(p)
        except:
            price.append('')

    # Парсинг количества книг. 
        try:
            cnt = soup.find('i',('class','icon-ok')).text
            # cnt = int(re.sub('[^0-9]', '', cnt))
            count.append(cnt)
        except:
            count.append('')

        # Парсинг содержания.
    try:
        content.append(soup.find('div', ('class', 'sub-header')).text)
    except:
        content.append('')


    output = {'Name' : name, 'Price' : price, 'Count' : count, 'Content': content}

    if not next_page_link:
        break
    url = urllib.parse.urljoin('https://www.boxofficemojo.com', next_page_link)

print(output)

# сохранение данных в JSON-файл
# with open("booksshop.json", 'w') as f:
#         json.dump(output, f, indent=4)