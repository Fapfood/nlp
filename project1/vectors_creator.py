import pickle

from nltk.corpus import wordnet as wn

with open('../categories/a_c_dict', 'rb') as handle:
    A_C_DICT = pickle.loads(handle.read())
with open('../categories/c_a_dict', 'rb') as handle:
    C_A_DICT = pickle.loads(handle.read())


def frequencies_for_noun(noun):
    for adjective, tf in sorted(A_C_DICT[noun].items(), key=lambda x: x[1], reverse=True):
        df = sum(C_A_DICT[adjective].values())
        print('{}\t{}\t{}\t{}'.format(adjective, tf, df, tf / df))


def calculate_N(group_training_list, adjective):
    if C_A_DICT.get(adjective) is None:
        adjective_count = 0
    else:
        adjective_count = sum(C_A_DICT[adjective].values())

    tmp_sum = 0
    for noun in group_training_list:
        if A_C_DICT.get(noun) is None:
            continue
        noun_count = sum(A_C_DICT[noun].values())
        adjective_noun_count = A_C_DICT[noun].get(adjective, 0)
        tmp_sum += adjective_noun_count / noun_count

    return tmp_sum / (adjective_count * len(group_training_list))


def get_categories(word):
    synsets = wn.synsets(word, pos=wn.NOUN, lang='pol')
    # print([l.lemma_names('pol') for l in synsets])
    return [l.lexname() for l in synsets]


def best_category(categories):
    if len(categories) == 0:
        return None
    dic = dict()
    for category in categories:
        dic[category] = dic.get(category, 0) + 1
    lis = list()
    for category in categories:
        lis.append((category, dic[category]))
    return max(lis, key=lambda x: x[1])[0]


def initial_examples_in_categories(start_index=0, end_index=5):
    groups = {}
    for noun, val in A_C_DICT.items():
        occurrences = sum(val.values())
        categories = get_categories(noun)
        category = best_category(categories)
        lis = groups.get(category, [])
        lis.append((noun, occurrences))
        groups[category] = lis

    initial_groups = {}
    for category, items in groups.items():
        if category in [None, 'noun.Tops']:
            continue
        initial_groups[category] = [l[0] for l in
                                    sorted(items, key=lambda x: x[1], reverse=True)[start_index:end_index]]
        # print(category, initial_groups[category])
    return initial_groups


if __name__ == '__main__':
    INITIAL_GROUPS = initial_examples_in_categories()
    ADJECTIVE_LIST = list(C_A_DICT.keys())

    ADJECTIVES_GROUPS_N = {k: {} for k in ADJECTIVE_LIST}
    for group_name, group_values in INITIAL_GROUPS.items():
        for adjective in ADJECTIVE_LIST:
            n = calculate_N(group_values, adjective)
            ADJECTIVES_GROUPS_N[adjective][group_name] = n

    GROUP_VECTORS = {k: [] for k in INITIAL_GROUPS.keys()}
    for adjective, groups in ADJECTIVES_GROUPS_N.items():
        normaliser = sum(groups.values())
        if normaliser == 0:
            normaliser = 1
        for group_name, n in groups.items():
            GROUP_VECTORS[group_name].append(n / normaliser)

    with open('../categories/initial_groups', 'wb') as handle:
        pickle.dump(INITIAL_GROUPS, handle)
    with open('../categories/adjective_list', 'wb') as handle:
        pickle.dump(ADJECTIVE_LIST, handle)
    with open('../categories/group_vectors', 'wb') as handle:
        pickle.dump(GROUP_VECTORS, handle)

    TEST_GROUPS = initial_examples_in_categories(5, 10)
    with open('../categories/test_groups', 'wb') as handle:
        pickle.dump(TEST_GROUPS, handle)
