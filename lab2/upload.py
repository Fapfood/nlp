import glob

import requests


def for_one(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    name = name.replace('.txt', '').replace('../ustawy', '')[1:]

    url = 'http://localhost:9200/my_index/ustawa/{}'.format(name)
    headers = {'Content-Type': 'application/json'}
    data = {'content': content}

    response = requests.put(url=url, json=data, headers=headers)
    print(response.content)


for filename in glob.glob("../ustawy/*.txt"):
    for_one(filename)
