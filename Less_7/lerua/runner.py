from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lerua import settings
from lerua.spiders.ler import LerSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    search = 'almaznye-mozaiki'
    process.crawl(LerSpider, search=search)

    process.start()