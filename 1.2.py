# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json
#access_token=737c6abec967a9b8867805a53f2edb897ac7bcb270849ef73dfa344ef3837d49ff912fda8e4d5d13602e6&expires_in=86400&user_id=11758920

url = f"https://api.vk.com/method/friends.getOnline?v=5.131&access_token=737c6abec967a9b8867805a53f2edb897ac7bcb270849ef73dfa344ef3837d49ff912fda8e4d5d13602e6&expires_in=86400&user_id=11758920"
response = requests.get(url)
j_friends = response.json()

with open('friends.json', 'w') as friends:
    json.dump(j_friends, friends)


url_2 = f"https://api.vk.com/method/store.getStickersKeywords?v=5.131&access_token=737c6abec967a9b8867805a53f2edb897ac7bcb270849ef73dfa344ef3837d49ff912fda8e4d5d13602e6&expires_in=86400&user_id=11758920"
response_2 = requests.get(url_2)
j_stikers = response_2.json()

with open('stikers.json', 'w') as stikers:
    json.dump(j_stikers, stikers)


url_3 = f"https://api.vk.com/method/account.getBanned?v=5.131&access_token=737c6abec967a9b8867805a53f2edb897ac7bcb270849ef73dfa344ef3837d49ff912fda8e4d5d13602e6&expires_in=86400&user_id=11758920"
response_3 = requests.get(url_3)
j_ban = response_3.json()

with open('ban.json', 'w') as ban:
    json.dump(j_ban, ban)