import json

import math
import requests


def synsets(word):
    url = 'http://ws.clarin-pl.eu/lexrest/lex'

    headers = {'Content-Type': 'application/json'}
    data = {'task': 'all', 'tool': 'plwordnet', 'lexeme': word}

    response = requests.post(url=url, json=data, headers=headers)
    dct = json.loads(response.content)
    return dct['results']['synsets']


def synset(id):
    url = 'http://ws.clarin-pl.eu/lexrest/lex'

    headers = {'Content-Type': 'application/json'}
    data = {'task': 'synset', 'tool': 'plwordnet', 'id': str(id)}

    response = requests.post(url=url, json=data, headers=headers)
    dct = json.loads(response.content)
    return dct['results']


def synonyms(synset):
    return synset['str']
    print('SYNONYMS')
    print(synset['str'])
    for synonym in synset['units']:
        print(synonym['synset'], synonym['lemma'], end=', ')
    print('\b\b')


def hyponyms(synset):
    hps = synset['related'].get('hiperonimia', [])
    return hps
    print('HYPONYMS')
    for hyponym in hps:
        print(*hyponym)


def hypernyms(synset):
    hps = synset['related'].get('hiponimia', [])
    return hps
    print('HYPERNYMS')
    for hypernym in hps:
        print(*hypernym)


sss = synsets('szkoda')
for ss in sss:
    print(synonyms(ss))
print()

hp0 = synsets('wypadek drogowy')[0]
print(hp0)
print(hypernyms(hp0))
hp1 = synset(hypernyms(hp0)[0][0])
print(hp1)
print(hypernyms(hp1))
hp2 = synset(hypernyms(hp1)[0][0])
print(hp2)
print(hypernyms(hp2))
hp3 = synset(hypernyms(hp2)[0][0])
print(hp3)
print()

ss = synsets('wypadek')[2]
print(ss['str'])
hps = hyponyms(ss)
for hp in hps:
    hp = synset(hp[0])
    print("'-" + hp['str'])
    for hp2 in hyponyms(hp):
        print("  '-" + synset(hp2[0])['str'])
print()

print('szkoda2')
ss = synsets('szkoda')[0]
print(ss)
print('strata1')
ss = synsets('strata')[1]
print(ss)
print('uszczerbek1')
ss = synsets('uszczerbek')[0]
print(ss)
print('szkoda majątkowa1')
ss = synsets('szkoda majątkowa')[0]
print(ss)
print('uszczerbek na zdrowiu1')
ss = synsets('uszczerbek na zdrowiu')[0]
print(ss)
print('krzywda1')
ss = synsets('krzywda')[0]
print(ss)
print('niesprawiedliwość1')
ss = synsets('niesprawiedliwość')[2]
print(ss)
print('nieszczęście2')
ss = synsets('nieszczęście')[0]
print(ss)
print()

print('wypadek1')
ss = synsets('wypadek')[2]
print(ss)
print('wypadek komunikacyjny1')
ss = synsets('wypadek komunikacyjny')[0]
print(ss)
print('kolizja2')
ss = synsets('kolizja')[1]
print(ss)
print('zderzenie2')
ss = synsets('zderzenie')[1]
print(ss)
print('kolizja drogowa1')
ss = synsets('kolizja drogowa')[0]
print(ss)
print('bezkolizyjny2')
ss = synsets('bezkolizyjny')[1]
print(ss)
print('katastrofa budowlana1')
ss = synsets('katastrofa budowlana')[0]
print(ss)
print('wypadek drogowy1')
ss = synsets('wypadek drogowy')[0]
print(ss)
print()

hp0 = synsets('szkoda')[0]
print(hp0)
print(hypernyms(hp0))
hp1 = synset(hypernyms(hp0)[1][0])
print(hp1)
print(hypernyms(hp1))

D = 36
d1 = 5
d2 = 7
d3 = 8
print(math.log(2 * D) - math.log(d1))
print(math.log(2 * D) - math.log(d2))
print(math.log(2 * D) - math.log(d3))
