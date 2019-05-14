import glob
import random

import regex as re
from sklearn.model_selection import train_test_split


def first_cleanup(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    kind = re.search(r'o\s*zmianie\s*(ustawy|niektórych\s*ustaw)', content) is not None
    kind = 'amending' if kind else 'not'
    content = re.split(r'Art\.\s*\d+\.', content, 1)[1]
    content = '\n'.join([ll.rstrip() for ll in content.splitlines() if ll.strip()])

    name = name.replace('../ustawy', '')[1:]

    with open(kind + '/' + name, 'w', encoding='utf8') as f:
        f.write(content)


def second_split(name, label):
    with open(name, encoding='utf8') as f:
        content = f.read().splitlines()

    choise1 = content
    choise2 = random.sample(content, (len(content) // 10) + 1)
    if len(content) >= 10:
        choise3 = random.sample(content, 10)
    else:
        choise3 = choise1
    choise4 = random.sample(content, 1)

    choise1 = re.sub(r'\s+', ' ', ' '.join(choise1))
    choise2 = re.sub(r'\s+', ' ', ' '.join(choise2))
    choise3 = re.sub(r'\s+', ' ', ' '.join(choise3))
    choise4 = re.sub(r'\s+', ' ', ' '.join(choise4))

    with open('100%-{}-data.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write(choise1 + '\n')
    with open('10%-{}-data.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write(choise2 + '\n')
    with open('10-{}-data.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write(choise3 + '\n')
    with open('1-{}-data.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write(choise4 + '\n')

    with open('100%-{}-label.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write('__label__{}'.format(label) + '\n')
    with open('10%-{}-label.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write('__label__{}'.format(label) + '\n')
    with open('10-{}-label.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write('__label__{}'.format(label) + '\n')
    with open('1-{}-label.txt'.format(label), 'a+', encoding='utf8') as f:
        f.write('__label__{}'.format(label) + '\n')


def split_train_test_validate(label):
    with open('1-{}-data.txt'.format(label), encoding='utf8') as f:
        data1 = f.read().splitlines()
    with open('1-{}-label.txt'.format(label), encoding='utf8') as f:
        label1 = f.read().splitlines()
    with open('10-{}-data.txt'.format(label), encoding='utf8') as f:
        data2 = f.read().splitlines()
    with open('10-{}-label.txt'.format(label), encoding='utf8') as f:
        label2 = f.read().splitlines()
    with open('10%-{}-data.txt'.format(label), encoding='utf8') as f:
        data3 = f.read().splitlines()
    with open('10%-{}-label.txt'.format(label), encoding='utf8') as f:
        label3 = f.read().splitlines()
    with open('100%-{}-data.txt'.format(label), encoding='utf8') as f:
        data4 = f.read().splitlines()
    with open('100%-{}-label.txt'.format(label), encoding='utf8') as f:
        label4 = f.read().splitlines()

    datas = train_test_split(data1, label1, data2, label2, data3, label3, data4, label4, train_size=0.6)
    train_data1, train_label1, train_data2, train_label2, \
    train_data3, train_label3, train_data4, train_label4 = datas[::2]
    datas = train_test_split(*datas[1::2], train_size=0.5)
    validate_data1, validate_label1, validate_data2, validate_label2, \
    validate_data3, validate_label3, validate_data4, validate_label4 = datas[::2]
    test_data1, test_label1, test_data2, test_label2, \
    test_data3, test_label3, test_data4, test_label4 = datas[1::2]

    with open('train/1-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_data1) + '\n')
    with open('train/1-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_label1) + '\n')
    with open('train/10-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_data2) + '\n')
    with open('train/10-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_label2) + '\n')
    with open('train/10%-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_data3) + '\n')
    with open('train/10%-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_label3) + '\n')
    with open('train/100%-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_data4) + '\n')
    with open('train/100%-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(train_label4) + '\n')

    with open('validate/1-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_data1) + '\n')
    with open('validate/1-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_label1) + '\n')
    with open('validate/10-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_data2) + '\n')
    with open('validate/10-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_label2) + '\n')
    with open('validate/10%-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_data3) + '\n')
    with open('validate/10%-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_label3) + '\n')
    with open('validate/100%-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_data4) + '\n')
    with open('validate/100%-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(validate_label4) + '\n')

    with open('test/1-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_data1) + '\n')
    with open('test/1-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_label1) + '\n')
    with open('test/10-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_data2) + '\n')
    with open('test/10-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_label2) + '\n')
    with open('test/10%-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_data3) + '\n')
    with open('test/10%-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_label3) + '\n')
    with open('test/100%-data.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_data4) + '\n')
    with open('test/100%-label.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(test_label4) + '\n')


def prepare_fasttext(set_kind, part_kind):
    with open('{}/{}-data.txt'.format(set_kind, part_kind), encoding='utf8') as f:
        data = f.read().splitlines()

    with open('{}/{}-label.txt'.format(set_kind, part_kind), encoding='utf8') as f:
        labels = f.read().splitlines()

    for i, line in enumerate(data):
        labels[i] += ' ' + line

    content = '\n'.join(labels)

    with open('{}-{}.txt'.format(set_kind, part_kind), 'w', encoding='utf8') as f:
        f.write(content)


for filename in glob.glob("../ustawy/*.txt"):
    first_cleanup(filename)
for filename in glob.glob("amending/*.txt"):
    second_split(filename, 'amending')
for filename in glob.glob("not/*.txt"):
    second_split(filename, 'not')

split_train_test_validate('amending')
split_train_test_validate('not')

prepare_fasttext('test', '1')
prepare_fasttext('test', '10')
prepare_fasttext('test', '10%')
prepare_fasttext('test', '100%')

prepare_fasttext('train', '1')
prepare_fasttext('train', '10')
prepare_fasttext('train', '10%')
prepare_fasttext('train', '100%')

prepare_fasttext('validate', '1')
prepare_fasttext('validate', '10')
prepare_fasttext('validate', '10%')
prepare_fasttext('validate', '100%')
