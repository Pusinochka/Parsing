# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# • название источника;
# • наименование новости;
# • ссылку на новость;
# • дата публикации.
# Сложить собранные новости в БД

from pprint import pprint
import requests
from lxml import html
from pymongo import MongoClient


client = MongoClient('localhost',27017)

db = client['news_db']
news = db.news


url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

#топ-новость
name_top = dom.xpath(".//h3[@class='card-big__title']/text()")[0]
lin = dom.xpath(".//a[@class='card-big _topnews _news']/@href")[0]
link_top = url + str(lin)
time_top = dom.xpath(".//time[@class='card-big__date']/text()")[0]


doc = {
    "source": url,
    "name": name_top,
    "link": link_top,
    "time": time_top,
}

news.update_one(doc, {'$set': doc}, upsert=True)

#остальные 12 новостей из главного блока
news_items = dom.xpath("//a[@class='card-mini _topnews']")
for item in news_items:
    name = item.xpath(".//span[@class='card-mini__title']/text()")
    l = item.xpath(".//@href")
    link = url + str(l[0])
    time = item.xpath(".//time[@class='card-mini__date']/text()")

    doc = {
        "source": url,
        "name": name,
        "link": link,
        "time": time,
    }
    news.update_one(doc, {'$set': doc}, upsert=True)


for doc in news.find({}):
    pprint(doc)