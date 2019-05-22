import numpy as np
from matplotlib import pyplot as plt


def histogram(data):
    word, frequency = zip(*data)
    indices = np.arange(len(data))
    plt.bar(indices, frequency, color='r')
    plt.xticks(indices, word, rotation='vertical')
    plt.tight_layout()
    plt.show()


with open('tmp_dict', encoding='utf8') as f:
    content = f.read()

dct = eval(content)

dct1 = {}
for d in dct:
    v = sum(dct[d].values())
    dct1[d] = v

res1 = sorted(dct1.items(), key=lambda x: x[1], reverse=True)

for d in res1:
    print(d)

histogram(res1)

print()

dct2 = {}
for d in dct:
    k = d[0:7]
    dct2[k] = dct2.get(k, 0) + dct1[d]

res2 = sorted(dct2.items(), key=lambda x: x[1], reverse=True)

for d in res2:
    print(d)

histogram(res2)

print()

dct3 = {}
for d in dct:
    for c in dct[d]:
        k = (c, d)
        dct3[k] = dct[d][c]

res3 = sorted(dct3.items(), key=lambda x: x[1], reverse=True)[:50]

for d in res3:
    print(d)

print()

dct4 = {}
for d in dct:
    k = d[0:7]
    dct4[k] = dct4.get(k, {})
    dct4[k][d] = dct[d]

for z in dct4:
    dct5 = {}
    for d in dct4[z]:
        for c in dct4[z][d]:
            k = (c, d)
            dct5[k] = dct4[z][d][c]

    res5 = sorted(dct5.items(), key=lambda x: x[1], reverse=True)[:10]

    print(z)
    for d in res5:
        print(d)
    print()
