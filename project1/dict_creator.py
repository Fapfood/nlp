import pickle

CASES = ('M', 'D', 'C', 'B', 'N', 'Msc', 'W')
GENDERS = ('lp_m_zyw_os', 'lp_m_zyw_nos', 'lp_m_nzyw', 'lp_zen', 'lp_nij', 'lmn_mos', 'lmn_nmos')


def add_base_to_vector(base, vector):
    return [base + el if el != '*' else '' for el in vector]


def grammatical_gender_a(code, plural=False):
    if not plural:
        if int(code[1]) < 6:
            return int(code[1])
        else:
            return None
    else:
        if code[1] == '1':
            return 6
        else:
            return 7


def add_elems_from_vector_to_dict(dic, word, vector, gender):
    if gender is None:
        return
    for num, el in enumerate(vector):
        record = ((CASES[num], GENDERS[gender - 1]), word)
        lis = dic.get(el, list())
        lis.append(record)
        dic[el] = lis


def create_a_dict(a_dict):
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

        # print(singular[0], grammatical_gender_a(code, False), singular)
        # print(plural[0], grammatical_gender_a(code, True), plural)

        add_elems_from_vector_to_dict(a_dict, word, singular, grammatical_gender_a(code, False))
        add_elems_from_vector_to_dict(a_dict, word, plural, grammatical_gender_a(code, True))


def create_c_dict(c_dict):
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

        # print(lp_m_zyw_os[0], 1, lp_m_zyw_os)
        # print(lp_m_zyw_nos[0], 2, lp_m_zyw_nos)
        # print(lp_m_nzyw[0], 3, lp_m_nzyw)
        # print(lp_zen[0], 4, lp_zen)
        # print(lp_nij[0], 5, lp_nij)
        # print(lmn_mos[0], 6, lmn_mos)
        # print(lmn_nmos[0], 7, lmn_nmos)

        add_elems_from_vector_to_dict(c_dict, word, lp_m_zyw_os, 1)
        add_elems_from_vector_to_dict(c_dict, word, lp_m_zyw_nos, 2)
        add_elems_from_vector_to_dict(c_dict, word, lp_m_nzyw, 3)
        add_elems_from_vector_to_dict(c_dict, word, lp_zen, 4)
        add_elems_from_vector_to_dict(c_dict, word, lp_nij, 5)
        add_elems_from_vector_to_dict(c_dict, word, lmn_mos, 6)
        add_elems_from_vector_to_dict(c_dict, word, lmn_nmos, 7)


def add_words(word_list, a_c_dict, c_a_dict, a_dict, c_dict, search_number=3):
    for i, word in enumerate(word_list):
        a_list = a_dict.get(word)
        if a_list is None:
            continue
        for j in list(range(i - search_number, i)) + list(range(i + 1, i + search_number + 1)):
            if j < 0 or j >= len(word_list):
                continue
            c_list = c_dict.get(word_list[j])
            if c_list is None:
                continue
            tmp_set = set()
            for a_entity in a_list:
                for c_entity in c_list:
                    if a_entity[0] == c_entity[0]:
                        tmp_set.add((c_entity[1], a_entity[1]))
            if len(tmp_set) > 0:
                c, a = tmp_set.pop()

                tmp_c_dict = a_c_dict.get(a, {})
                a_c_dict[a] = tmp_c_dict
                tmp_c_count = tmp_c_dict.get(c, 0)
                tmp_c_dict[c] = tmp_c_count + 1

                tmp_a_dict = c_a_dict.get(c, {})
                c_a_dict[c] = tmp_a_dict
                tmp_a_count = tmp_a_dict.get(a, 0)
                tmp_a_dict[a] = tmp_a_count + 1


if __name__ == '__main__':
    A_DICT = {}
    create_a_dict(A_DICT)

    C_DICT = {}
    create_c_dict(C_DICT)

    A_C_DICT = {}
    C_A_DICT = {}

    with open('../categories/tokens-with-entities.tsv', encoding='utf8') as f:
        sentence = []
        for i, line in enumerate(f):
            # if i > 1_000_000:
            #     break
            line = line[:-1]
            if line == '':
                add_words(sentence, A_C_DICT, C_A_DICT, A_DICT, C_DICT)
                sentence = []
            else:
                word = line.lower().split('\t')[1]
                sentence.append(word)

    with open('../categories/a_c_dict', 'wb') as handle:
        pickle.dump(A_C_DICT, handle)
    with open('../categories/c_a_dict', 'wb') as handle:
        pickle.dump(C_A_DICT, handle)

# A (rzeczownik) lub C (przymiotnik)
# Dla AXYZ: X - rodzaj, Y - 1-pospolity 2-nazwa własna, Z - które znaczenie
# Dla CXYZ: X - stopień (tylko dla przymiotnika), Y - które znaczenie(?), Z - 1-przymiotnik 2-imieslow przymiotnikowy czynny (ący, ąca, ące, ły, ła, łe) 3-imieslow przymiotnikowy bierny (ny, na, ne, ty, ta, te)

# nudzenie;A511
# nudzenie;A512
# krakowiak;A111
# krakowiak;A121
# krakowiak;A211
# warsztatowiec;A111
# warsztatowiec;A311

# abstrakcyjny;C111
# abstrakcyjniejszy;C211
# najabstrakcyjniejszy;C311
# ablacyjny;C111
# ablaktowany;C113
# ablaktujący;C112
# adapterowy;C111
# adaptowany;C113
# adaptujący;C112
# adaptujący;C122

# nożyce;A711;nożyc:e:*:*:*:*:*:*:*:e::om:e:ami:ach:e:
