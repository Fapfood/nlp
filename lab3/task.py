import csv
import json

import editdistance
import matplotlib.pyplot as plt


def plot(ranked):
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)

    a = [l[1] for l in ranked]
    line, = ax.plot(a)
    ax.set_yscale('log')

    plt.show()


with open('dict.json') as f:
    content = f.read()

dct = json.loads(content)
lst = sorted(dct.items(), key=lambda x: (-x[1], x[0]))
print(len(lst))
print(lst)

plot(lst)

with open('../polimorfologik-2.1/polimorfologik-2.1.txt', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=';')
    morfologik = [(rows[0].lower(), rows[1].lower()) for rows in reader]
    morfologik = set([item for sublist in morfologik for item in sublist])

strange_words = [elem for elem in lst if elem[0] not in morfologik]

print(len(strange_words))
print(strange_words)

print(strange_words[:30])
levenshtein = [word[0] for word in strange_words if word[1] == 3]
print(len(levenshtein))
print(levenshtein[:30])

base_list = [l[0] for l in lst if l not in strange_words]
print(len(base_list))
print(base_list)

for example in levenshtein[:30]:
    min_distance = float('inf')
    found = None
    for base in base_list:
        distance = editdistance.eval(example, base)
        if distance < min_distance:
            min_distance = distance
            found = base
        if distance == 1:
            break
    print(example, found, min_distance)
