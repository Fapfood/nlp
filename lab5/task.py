import glob

import math
import regex as re
import requests

COUNTER = {}
FIRST = {}
SECOND = {}
ALL = 0


def entropy(counts):
    return sum([k / ALL * math.log(k / ALL + (k == 0)) for k in counts])


def for_one(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'^\s+', '', content)

    url = 'http://localhost:9200'

    response = requests.post(url=url, data=content.encode('utf-8')).content.decode('utf-8')
    lines = response.splitlines()

    terms = []
    tmp_term = None
    tmp_cases = None
    for line in lines:
        line = line.split('\t')
        if len(line) == 2:
            terms.append((tmp_term, tmp_cases))
            tmp_term = line[0]
            tmp_cases = []
        elif len(line) == 4:
            tmp_cases.append((line[1], line[2].split(':')[0]))

    terms = terms[1:]

    sum = 0
    for i, elem in enumerate(terms[1:]):
        if elem[0].isalpha() and terms[i][0].isalpha():
            key1 = terms[i][1][0]
            FIRST[key1] = FIRST.get(key1, 0) + 1
            key2 = elem[1][0]
            SECOND[key2] = SECOND.get(key2, 0) + 1
            key = (key1, key2)
            COUNTER[key] = COUNTER.get(key, 0) + 1
            sum += 1
    return sum


for filename in glob.glob("../ustawy/*.txt"):
    ALL += for_one(filename)

LLR = []
for key, val in COUNTER.items():
    k_11 = val
    k_12 = SECOND[key[1]] - val
    k_21 = FIRST[key[0]] - val
    k_22 = ALL - k_11 - k_12 - k_21
    llr = 2 * ALL * (entropy([k_11, k_12, k_21, k_22]) -
                     entropy([k_11 + k_12, k_21 + k_22]) -
                     entropy([k_11 + k_21, k_12 + k_22]))
    LLR.append((key, llr))

LLR.sort(key=lambda x: x[1])
LLR = list(filter(lambda x: x[0][0][1] == 'subst' and x[0][1][1] in ['subst', 'adj'], LLR))
print(LLR[-50:])
