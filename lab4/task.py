import regex as re
import glob
import math

COUNTER = {}
FIRST = {}
SECOND = {}
ALL = 0


def entropy(counts):
    return sum([k / ALL * math.log(k / ALL + (k == 0)) for k in counts])


def for_one(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    content = re.sub(r'[[[:punct:]]', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'^\s+', '', content)
    content = content.lower()
    terms = content.split(' ')

    sum = 0
    for i, elem in enumerate(terms[1:]):
        if elem.isalpha() and terms[i].isalpha():
            key1 = terms[i]
            FIRST[key1] = FIRST.get(key1, 0) + 1
            key2 = elem
            SECOND[key2] = SECOND.get(key2, 0) + 1
            key = (terms[i], elem)
            COUNTER[key] = COUNTER.get(key, 0) + 1
            sum += 1
    return sum


for filename in glob.glob("../ustawy/*.txt"):
    ALL += for_one(filename)

PMI = []
LLR = []
for key, val in COUNTER.items():
    pmi = math.log(val / (FIRST[key[0]] * SECOND[key[1]]))
    k_11 = val
    k_12 = SECOND[key[1]] - val
    k_21 = FIRST[key[0]] - val
    k_22 = ALL - k_11 - k_12 - k_21
    llr = 2 * ALL * (entropy([k_11, k_12, k_21, k_22]) -
                     entropy([k_11 + k_12, k_21 + k_22]) -
                     entropy([k_11 + k_21, k_12 + k_22]))
    PMI.append((key, pmi))
    LLR.append((key, llr))

PMI.sort(key=lambda x: x[1])
LLR.sort(key=lambda x: x[1])
print(PMI[:30])
print(PMI[-30:])
print(LLR[:30])
print(LLR[-30:])
