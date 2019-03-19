import regex as re
import glob

COUNTER = {}


def for_one(name):
    with open(name, encoding='utf8') as f:
        content = f.read()

    main = re.findall(r'((Dz\.\s*U\.)(\s*z\s*\d{4}\s*r\.)(\s*Nr\s*\d+,\s*poz\.\s*\d+))\s*USTAWA', content)
    if len(main) > 0:
        main_year = re.sub(r'\s*', '', main[0][2])
    else:
        main_year = 'NNone'

    a = re.findall(r'((Dz\.\s*U\.)((\s*z\s*\d{4}\s*r\.)?((\s*Nr\s*\d+,\s*poz\.\s*\d+)(,|\s*i)?)+(\s*oraz)?)+)', content,
                   flags=re.MULTILINE)
    for elem in a:
        elem = re.sub(r'\s*', '', elem[0])
        b = re.findall(r'((Dz\.U\.)?(z\d{4}r\.)?((Nr\d+,poz\.\d+)(,|i)?)+(oraz)?)', elem)
        for elem2 in b:
            year = elem2[2] if elem2[2] != '' else main_year
            elem2 = elem2[0].replace('Dz.U.', '').replace('oraz', '').replace(year, '')
            c = re.findall(r'(Nr\d+,poz\.\d+)(,|i)?', elem2)
            year = year[1:5]
            for elem3 in c:
                elem3 = elem3[0]
                number, position = elem3.split(',')
                number = number[2:]
                position = position[4:]
                key = (year, number, position)
                COUNTER[key] = COUNTER.get(key, 0) + 1


for filename in glob.glob("../ustawy/*.txt"):
    for_one(filename)

sort = sorted(COUNTER.items(), key=lambda x: x[1], reverse=True)
print(sort)
