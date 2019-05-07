from random import sample

import matplotlib.pyplot as plt
import numpy as np
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE

MODEL = KeyedVectors.load_word2vec_format('../skipgram/skip_gram_v100m8.w2v.txt', binary=False)


def get_vector(word):
    token = word.replace(' ', '_') + '::noun'
    try:
        vector = MODEL.get_vector(token)
    except Exception as e:
        print(e)
        vector = None
    return vector


def most_similar(word, topn=5):
    token = get_vector(word)
    if token is not None:
        return MODEL.similar_by_vector(token, topn=topn)


def calculate(word1, word2, word3, topn=5):
    token1 = get_vector(word1)
    token2 = get_vector(word2)
    token3 = get_vector(word3)
    if token1 is not None and token2 is not None and token3 is not None:
        return MODEL.similar_by_vector(token1 - token2 + token3, topn=topn)


def tsne_plot(words, k=1000):
    random_tokens = sample(MODEL.vocab.keys(), k=k)
    random_embedings = [MODEL.get_vector(x) for x in random_tokens]
    selected_embedings = [get_vector(x) for x in words if get_vector(x) is not None]
    embedings = np.array(random_embedings + selected_embedings)
    x = TSNE().fit_transform(embedings)
    c = np.concatenate([
        np.zeros(len(random_embedings)),
        np.ones(len(selected_embedings))
    ])
    plt.figure(figsize=(16, 16))
    plt.scatter(x[:, 0], x[:, 1], c=c)
    plt.show()


t1 = ['sąd wysoki',
      'trybunał konstytucyjny',
      'kodeks cywilny',
      'kpk',
      'sąd rejonowy',
      'szkoda',
      'wypadek',
      'kolizja',
      'szkoda majątkowy',
      'nieszczęście',
      'rozwód']

for t in t1:
    print(most_similar(t))

t2 = [('sąd wysoki', 'kpc', 'konstytucja'),
      ('pasażer', 'mężczyzna', 'kobieta'),
      ('samochód', 'droga', 'rzeka'),
      ('król', 'mężczyzna', 'kobieta')]

for t in t2:
    print(calculate(*t))

t3 = ['szkoda',
      'strata',
      'uszczerbek',
      'szkoda majątkowy',
      'uszczerbek na zdrowie',
      'krzywda',
      'niesprawiedliwość',
      'nieszczęście']

tsne_plot(t3)
