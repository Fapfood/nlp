import glob
import json

import requests


def for_one(name):
    name = name.replace('.txt', '').replace('../ustawy', '')[1:]

    url = 'http://localhost:9200/my_index/ustawa/{}/_termvectors?fields=content'.format(name)

    response = requests.get(url=url)
    dct = json.loads(response.content)
    terms = dct['term_vectors']['content']['terms']
    terms = [(t[0], t[1]['term_freq']) for t in terms.items() if t[0].isalpha() and len(t[0]) >= 2]

    return terms


global_dct = {}
for filename in glob.glob('../ustawy/*.txt'):
    terms = for_one(filename)
    for key, value in terms:
        global_dct[key] = global_dct.get(key, 0) + value

with open('dict.json', 'w') as f:
    f.write(json.dumps(global_dct))
