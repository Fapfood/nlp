import pickle

from project1.vectors_creator import calculate_N, get_categories, best_category

with open('../categories/initial_groups', 'rb') as handle:
    INITIAL_GROUPS = pickle.loads(handle.read())
with open('../categories/adjective_list', 'rb') as handle:
    ADJECTIVE_LIST = pickle.loads(handle.read())
with open('../categories/group_vectors', 'rb') as handle:
    GROUP_VECTORS = pickle.loads(handle.read())
with open('../categories/test_groups', 'rb') as handle:
    TEST_GROUPS = pickle.loads(handle.read())
with open('../categories/a_c_dict', 'rb') as handle:
    A_C_DICT = pickle.loads(handle.read())


def vector_for_word(word, adjective_list):
    vector = []
    for adjective in adjective_list:
        n = calculate_N([word], adjective)
        vector.append(n)
    return vector


def distance(v1, v2):
    scalar_product = 0
    for i, val in enumerate(v1):
        scalar_product += val * v2[i]
    len_v1 = (sum(map(lambda x: x ** 2, v1))) ** (1 / 2)
    len_v2 = (sum(map(lambda x: x ** 2, v2))) ** (1 / 2)
    if len_v2 == 0 or len_v1 == 0:
        return 0
    return scalar_product / (len_v1 * len_v2)


def best_match(word, adjective_list, group_vectors):
    vector = vector_for_word(word, adjective_list)
    distances = []
    for group_name, group_vector in group_vectors.items():
        d = distance(vector, group_vector)
        distances.append((group_name, d))
    best = [l[0] for l in sorted(distances, key=lambda x: x[1], reverse=True)[:5]]
    return best


def test(word):
    count = sum(A_C_DICT.get(word).values())
    print(word, count, best_match(word, ADJECTIVE_LIST, GROUP_VECTORS), get_categories(word))


ENG_PL = {
    'noun.Tops': 'bhp',  # unique beginner for nouns / najwyższy w hierarchii
    'noun.act': 'czy',  # acts or actions / czyn lub czynność
    'noun.animal': 'zw',  # animals /  zwierzęta
    'noun.artifact': 'wytw',  # man-made objects / wytwory (przedmiotowe i umysłowe)
    'noun.attribute': 'cech',  # attributes of people and objects / cechy (ludzi, zwierząt, rzeczy)
    'noun.body': 'czc',  # body parts / części ciała
    'noun.cognition': 'umy',  # cognitive processes and contents / myślenie, ocena, zwątpienie
    'noun.communication': 'por',  # communicative processes and contents / porozumiewanie się, komunikacja
    'noun.event': 'zdarz',  # natural events / zdarzenia
    'noun.feeling': 'czuj',  # feelings and emotions / uczucia, odczucia i emocje
    'noun.food': 'jedz',  # foods and drinks / jedzenie i picie
    'noun.group': 'grp',  # groupings of people or objects / grupy (ludzi, zwierząt, rzeczy)
    'noun.location': 'msc',  # spatial position / miejsca i umiejscowienie
    'noun.motive': 'cel',  # goals / cel lub motyw
    'noun.object': 'rz',  # natural objects ( not man-made) / obiekty naturalne
    'noun.person': 'os',  # people / ludzie
    'noun.phenomenon': 'zj',  # natural phenomena / zjawiska naturalne
    'noun.plant': 'rsl',  # plants / rośliny
    'noun.possession': 'pos',  # possession and transfer of possession / posiadanie i jego zmiana
    'noun.process': 'prc',  # natural processes / procesy naturalne
    'noun.quantity': 'il',  # quantities and units of measure / ilość, liczebność, jednostki miary
    'noun.relation': 'zwz',  # relations between people or things or ideas / związki (między ludźmi, rzeczami, ideami)
    'noun.shape': 'ksz',  # two and three dimensional shapes / kształty
    'noun.state': 'st',  # stable states of affairs / sytuacje statyczne (stany)
    'noun.substance': 'sbst',  # substances / substancja, materiał
    'noun.time': 'czas',  # time and temporal relations / czas i stosunki czasowe
}


def save_words():
    list = []
    for word, values in A_C_DICT.items():
        values = sum(values.values())
        list.append((word, values))
    list.sort(key=lambda x: x[1], reverse=True)

    with open('results.txt', 'w', encoding='utf8') as f:
        for word, count in list:
            best = best_match(word, ADJECTIVE_LIST, GROUP_VECTORS)
            correct = get_categories(word)
            max_correct = best_category(correct)
            f.write(
                'word:{}\tcount:{}\tis_correct:{}\tbest:{}\tcorrect:{}\n'.format(word, count, best[0] == max_correct,
                                                                                 best, correct))


if __name__ == '__main__':
    for category, items in INITIAL_GROUPS.items():
        print(category, items)
    print()

    for category, items in TEST_GROUPS.items():
        print('----{}----'.format(category))
        for item in items:
            test(item)

    print()
    test('pies')
    test('mieszkanie')
    test('głowa')
    test('frytka')
    test('przyjaźń')
    test('ogórek')
    test('jabłko')
    test('zerwanie')
    test('rozwód')
    test('kupa')
    test('twarz')
    test('poczta')
    test('tęcza')
    test('koń')
    test('zdanie')
    test('lekarz')
    test('kwadrat')
    test('tuzin')
    test('smutek')
    test('lato')
    test('wrzesień')
    test('uczciwość')
    test('nekrofilia')

    while True:
        test(input())
