# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0403


    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary = item['salary']
            salary = [re.sub('\xa0', "", s) for s in salary]

            if salary[0] == 'з/п не указана':
                min = None
                max = None
                cur = None
            elif salary[0] == 'от ':
                if salary[2] == ' до ':
                    min = salary[1]
                    min = int(min)
                    max = salary[3]
                    max = int(max)
                    cur = salary[-2]
                else:
                    max = None
                    min = salary[1]
                    min = int(min)
                    cur = salary[-2]
            elif salary[0] == 'до ':
                min = None
                max = salary[1]
                max = int(max)
                cur = salary[-2]

            item['min'] = min
            item['max'] = max
            item['cur'] = cur
            del item['salary']




        elif spider.name == 'sjru':
            salary = item['salary']
            salary = [re.sub('\xa0', "", s) for s in salary]
            salary = [re.sub('руб.', "", s) for s in salary]

            if salary[0] == 'По договорённости':
                min = None
                max = None
                cur = None
            elif salary[0] == 'от':
                max = None
                min = salary[2]
                min = int(min)
                cur = 'руб'
            elif salary[0] == 'до':
                min = None
                max = salary[2]
                max = int(max)
                cur = 'руб'
            else:
                min = salary[0]
                min = int(min)
                max = salary[1]
                max = int(max)
                cur = 'руб'

            item['min'] = min
            item['max'] = max
            item['cur'] = cur
            del item['salary']


        collections = self.mongobase[spider.name]
        collections.insert_one(item)
        return item