import glob
import json
import random
import time
import xml.etree.ElementTree as et

import regex as re
import requests

DIC = {}


def read_and_clean(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    content = re.sub(r'\s+', ' ', content)

    return content


def ner(sentence):
    url = 'http://ws.clarin-pl.eu/nlprest2/base/startTask'

    headers = {'Content-Type': 'application/json', 'Referer': 'http://ws.clarin-pl.eu/ner.shtml'}
    data = {'lpmn': 'any2txt|wcrft2|liner2({"model":"n82"})', 'application': 'ws.clarin-pl.eu', 'user': 'demo',
            'text': sentence}

    response = requests.post(url=url, json=data, headers=headers)
    task_id = response.content.decode('utf8')

    while True:
        url = 'http://ws.clarin-pl.eu/nlprest2/base/getStatus/{}'.format(task_id)
        response = requests.get(url=url)
        dct = json.loads(response.content)
        if dct['status'] == 'DONE':
            result_id = dct['value'][0]['fileID']
            break
        else:
            print('Processing...: {}'.format(dct['value']))
            time.sleep(1)

    url = 'http://ws.clarin-pl.eu/nlprest2/base/download{}'.format(result_id)
    response = requests.get(url=url)

    content = response.content.decode('utf8')
    root = et.fromstring(content)

    dic = {}
    for chunk in root:
        chunk_id = chunk.attrib['id']
        for sentence in chunk:
            sentence_id = sentence.attrib['id']
            for token in sentence:
                if token.tag == 'tok':
                    text = None
                    anns = []
                    for ann in token:
                        if ann.tag == 'orth':
                            text = ann.text
                        # if ann.tag == 'lex':
                        #     if ann.attrib['disamb'] == '1':
                        #         for lex in ann:
                        #             if lex.tag == 'base':
                        #                 base = lex.text
                        if ann.tag == 'ann':
                            if ann.text != '0':
                                anns.append((ann.attrib['chan'], chunk_id, sentence_id, ann.text))
                    for ann in anns:
                        dic[ann] = dic.get(ann, '') + text + ' '

    for k, v in dic.items():
        DIC[k[0]] = DIC.get(k[0], {})
        DIC[k[0]][v] = DIC[k[0]].get(v, 0) + 1

    return dic


random.seed(0)
for filename in random.sample(glob.glob("../ustawy/*.txt"), k=100):
    print(filename)
    text = read_and_clean(filename)
    res = ner(text)
    print(res)

# res = ner('Kraków jest w Polsce. Berlin jest w Niemczech, a nie w Polsce.')

print(DIC)
