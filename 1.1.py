# _ 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

username = 'Pusinochka'
token = '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'

repos = requests.get('https://api.github.com/user/repos', auth=(username, token))
repos_j = repos.json()

with open('repositories.json', 'w') as write_js:
    json.dump(repos_j, write_js)

for repo in repos.json():
    print(repo['full_name'])

