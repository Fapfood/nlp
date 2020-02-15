from project1.dict_creator import add_base_to_vector, grammatical_gender_a


def create_a_dict(dic):
    with open('../categories/class_a.txt', encoding='utf8') as f:
        lines = f.read().splitlines()
    for line in lines:
        word, code, vector = line.split(';')
        vector = vector.split(':')[:-1]
        base = vector[0]
        base_ending = vector[1]
        vector = add_base_to_vector(base, vector[2:])

        singular = vector[0:7]
        plural = vector[7:14]

        dic[singular[0]] = (grammatical_gender_a(code, False), singular)
        dic[plural[0]] = (grammatical_gender_a(code, True), plural)


def create_b_dict(dic):
    with open('../categories/class_b.txt', encoding='utf8') as f:
        lines = f.read().splitlines()
    for line in lines:
        word, vector = line.split(';')
        vector = vector.split(':')[:-1]
        base = vector[0]
        base_ending = vector[1]
        vector = add_base_to_vector(base, vector[2:])

        infinitive = vector[0:1]
        present = vector[1:7]
        imperative = vector[7:12]
        imieslowy1 = vector[12:14]
        past = vector[14:29]
        subjunctive = vector[29:44]
        impersonal_past = vector[44:45]
        imieslowy2 = vector[45:47]

        dic[word] = present + imperative + subjunctive


def create_c_plus_dict(dic):
    with open('../categories/class_c.txt', encoding='utf8') as f:
        lines = f.read().splitlines()
    for line in lines:
        word, code, vector = line.split(';')
        vector = vector.split(':')[:-3]
        base = vector[0]
        base_ending = vector[1]
        vector = add_base_to_vector(base, vector[2:])

        lp_m_zyw_os = vector[0:7]
        lp_m_zyw_nos = vector[0:7]
        lp_m_nzyw = vector[7:14]
        lp_zen = vector[14:21]
        lp_nij = vector[21:28]
        lmn_mos = vector[28:35]
        lmn_nmos = vector[35:42]

        def helper(vec, num):
            dic2 = dic.get(vec[0], dict())
            dic[vec[0]] = dic2
            dic2[num] = vec

        helper(lp_m_zyw_os, 1)
        helper(lp_m_zyw_nos, 2)
        helper(lp_m_nzyw, 3)
        helper(lp_zen, 4)
        helper(lp_nij, 5)
        helper(lmn_mos, 6)
        helper(lmn_nmos, 7)


def create_c_dict(dic):
    with open('../categories/class_c.txt', encoding='utf8') as f:
        lines = f.read().splitlines()
    for line in lines:
        word, code, vector = line.split(';')
        vector = vector.split(':')[:-3]
        base = vector[0]
        base_ending = vector[1]
        vector = add_base_to_vector(base, vector[2:])

        lp_m_zyw_os = vector[0:7]
        lp_m_zyw_nos = vector[0:7]
        lp_m_nzyw = vector[7:14]
        lp_zen = vector[14:21]
        lp_nij = vector[21:28]
        lmn_mos = vector[28:35]
        lmn_nmos = vector[35:42]

        lis = dic.get(word, list())
        dic[word] = lis

        lis += lp_m_zyw_os
        lis += lp_m_zyw_nos
        lis += lp_m_nzyw
        lis += lp_zen
        lis += lp_nij
        lis += lmn_mos
        lis += lmn_nmos


def merge(lis):
    """[('a','b'),('c','d')] -> ['a b','c d']"""
    res = []
    for l in lis:
        res.append(' '.join(l))
    return res


def swap(lis):
    """[('a','b','c')] -> [('a','b','c'),('b','c','a')]"""
    res = []
    for l in lis:
        res.append(l)
        res.append(l[1:] + l[:1])
    return res


def limit(lis):
    """['a','b','a',''] -> ['a','b']"""
    return list(sorted(list(set(lis) - {''})))


def flat(lis):
    """[('a','b'),('c')] -> ['a','b','c']"""
    return [item for sublist in lis for item in sublist]


def flat2(lis):
    """[(('a','b'),('c')),(('d'),('e'))] -> [('a','b','c'),('d','e')]"""
    return list(map(lambda x: x[0] + x[1], lis))


def adjective_noun_inflection(words):
    """Get list of two words: adjective and noun,
    return list of tuples of zipped word's forms"""
    adj = words[0]
    noun = words[1]
    noun = A_DICT[noun]
    adj = C_PLUS_DICT[adj][noun[0]]
    res = list(zip(adj, noun[1]))
    return res


def noun_inflection(words):
    """Get single-item list of verb,
    return list of single-item tuples of verb's forms"""
    noun = words[0]
    res = [(n,) for n in A_DICT[noun][1]]
    return res


def verb_inflection(words):
    """Get single-item list of verb,
    return list of single-item tuples of verb's forms"""
    verb = words[0]
    res = [(v,) for v in B_DICT[verb]]
    return res


def adjectives_inflection(words):
    """Get list of adjectives,
    return list of tuples of zipped adjective's forms"""
    res = [C_DICT[adj] for adj in words]
    return list(zip(*res))


def statics_inflection(words):
    """Get list of statics (words with only one correct form),
    return list of single-item tuples of static words"""
    return [(*words,)]


def inflection(words, type):
    """Get string of words,
    return list of strings of possible forms"""
    words = words.split()
    if type == 'adjective-noun':
        res = swap(adjective_noun_inflection(words))
    elif type == 'verb':
        res = verb_inflection(words)
    elif type == 'adjectives':
        res = adjectives_inflection(words)
    elif type == 'noun':
        res = noun_inflection(words)
    elif type == 'statics':
        res = statics_inflection(words)
    elif type == 'adjective-noun-statics':
        res1 = swap(adjective_noun_inflection(words[:2]))
        res2 = statics_inflection(words[2:]) * len(res1)
        res = flat2(list(zip(res1, res2)))
    elif type == 'noun-statics':
        res1 = swap(noun_inflection(words[:1]))
        res2 = statics_inflection(words[1:]) * len(res1)
        res = flat2(list(zip(res1, res2)))
    else:
        res = [words]
    return limit(merge(res))


A_DICT = {}
create_a_dict(A_DICT)

B_DICT = {}
create_b_dict(B_DICT)

C_DICT = {}
create_c_dict(C_DICT)

C_PLUS_DICT = {}
create_c_plus_dict(C_PLUS_DICT)

if __name__ == '__main__':
    print(inflection('dwudziesty drugi', 'adjectives'))
    print(inflection('pokój na strychu', 'noun-statics'))
    print(inflection('kochać', 'verb'))
    print(inflection('czerwony samochód', 'adjective-noun'))
    print(inflection('duża paczka na poczcie', 'adjective-noun-statics'))
    print(inflection('pies', 'noun'))
    print(inflection('tivi', 'statics'))
