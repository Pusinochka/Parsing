# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии/продукты в вашу базу.


import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('localhost',27017)

db = client['vacancies_db']
jobs = db.jobs

def hh(vacancy, page_sum):
    jobs_list = []

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}
    base_url = 'https://hh.ru'
    url = 'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&text=' + vacancy
    i = 1

    while i <= page_sum:
        response = requests.get(url, headers=headers)
        if response.ok:
            dom = BeautifulSoup(response.text, 'html.parser')
            jobs_block = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})


            for job in jobs_block:
                jobs_data = {}

            # название вакансии
                job_text = job.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                vacancy_name = job_text.getText()
                jobs_data['vacancy_name'] = vacancy_name

#                 # зп
                salary = job.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                if not salary:
                    salary_min = None
                    salary_max = None
                    salary_currency = None
                else:
                    salary = salary.getText().replace(u'\xa0', u'')
                    salary = re.split(r'\s|[, ]', salary)

                    if salary[0] == 'до':
                        salary_min = None
                        salary_max = salary[1] + salary[2]
                        salary_max = int(salary_max)
                    elif salary[0] == 'от':
                        salary_max = None
                        salary_min = salary[1] + salary[2]
                        salary_min = int(salary_min)
                    else:
                        salary_min = salary[0] + salary[1]
                        salary_min = int(salary_min)
                        salary_max = salary[3] + salary[4]
                        salary_max = int(salary_max)
                    salary_currency = salary[-1]
                jobs_data['salary_min'] = salary_min
                jobs_data['salary_max'] = salary_max
                jobs_data['salary_currency'] = salary_currency

                # ссылка на вакансию
                link_text = job.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                link = link_text['href']
                jobs_data['link'] = link
                jobs_data['site'] = base_url

                doc = {
                    "vacancy": vacancy_name,
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "currency": salary_currency,
                    "link": link,
                    "site": base_url
                }

                try:
                    jobs.update_one(doc, {'$set': doc}, upsert=True)
                except dke:
                    print('Duplicate key error collection')

                # jobs_list.append(jobs_data)

            page_text = dom.find('a', {'data-qa': 'pager-next'})
            if page_text:
                link_1 = page_text['href']
            else:
                break

        url = base_url + link_1

        i = i + 1

    df = pd.DataFrame(jobs_list)
    return df


hh('Python', 1)

for doc in jobs.find({}):
    print(doc)



# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).
def salary_want():
    salary = int(input('Введите минимальную зарплату: '))
    for doc in jobs.find({'$or': [{'salary_min': {'$gte': salary}}, {'salary_max': {'$gte': salary}}]}):
        print(doc)

salary_want()

