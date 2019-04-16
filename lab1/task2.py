import regex as re
import glob

wym = r'(wymienion(y|a|e|ego|ej|emu|ą|ym|ych|ymi)|wymienieni)\s*w'
okr = r'(określon(y|a|e|ego|ej|emu|ą|ym|ych|ymi)|określeni)\s*w'
zgd = r'zgodn(y|a|e|ego|ej|emu|ą|ym|ych|ymi|i|ie)\s*z'
matcher = r'(w\s*myśl|mowa\s*w|w\s*rozumieniu|na\s*podstawie|{WYM}|{OKR}|{ZGD})'.format(WYM=wym, OKR=okr, ZGD=zgd)
separator = r'\s*(lub|i|,|oraz)(\s*(w|z))?'
art = r'(\s*art\.((\s*\d+\s*-)?\s*\d+{SEP})*((\s*\d+\s*-)?\s*\d+))'.format(SEP=separator)
ust = r'(\s*(§|ust\.)((\s*\d+\s*-)?\s*\d+{SEP})*((\s*\d+\s*-)?\s*\d+))'.format(SEP=separator)
pkt = r'(\s*pkt((\s*\d+\s*-)?\s*\d+{SEP})*((\s*\d+\s*-)?\s*\d+))'.format(SEP=separator)
lit = r'(\s*lit\.((\s*\w+\s*-)?\s*\w+{SEP})*((\s*\w+\s*-)?\s*\w+))'.format(SEP=separator)
block = r'({ART}|{UST}|{PKT}|{LIT})+'.format(ART=art, UST=ust, PKT=pkt, LIT=lit)
regex = r'({MCH}({BL}{SEP})*{BL})'.format(SEP=separator, BL=block, MCH=matcher)


def for_one(name):
    COUNTER = {}
    TO_PROCESS = []

    with open(name, encoding='utf8') as f:
        content = f.read()

    founds = re.findall(regex, content, flags=re.M | re.I)
    for elem in founds:
        elem = re.sub(r'\s*', '', elem[0].replace(elem[1], '').replace('§', 'ust.'))
        arts = re.findall(art, elem)
        others = re.sub(art, 'SEP', elem).split('SEP')

        TO_PROCESS.append(('?', re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[0])))
        for i, a in enumerate(arts):
            f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=a[6]), '', a[0])
            while f != 'art.':
                f = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', f)
                f = re.findall(art, f)[0]
                TO_PROCESS.append(('ART', f[6]))
                f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=f[6]), '', f[0])
            other = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[i + 1])
            if other != '':
                TO_PROCESS.append(('ART+', a[6], other))
            else:
                TO_PROCESS.append(('ART', a[6]))

    UST_TO_PROCESS = []
    for elem in TO_PROCESS:
        if elem[0] == '?' and elem[1] == '':
            continue
        elif elem[0] == 'ART':
            key = elem[1]
            pref = 'ART '

            if len(key.split('-')) == 1:
                COUNTER[pref + key] = COUNTER.get(pref + key, 0) + 1
            else:
                for i in range(int(key.split('-')[0]), int(key.split('-')[1]) + 1):
                    COUNTER[pref + str(i)] = COUNTER.get(pref + str(i), 0) + 1
        elif elem[0] == 'ART+':
            UST_TO_PROCESS.append((('ART', elem[1]), elem[2]))
        elif elem[0] == '?':
            UST_TO_PROCESS.append(elem)

    TO_PROCESS = []
    for elem in UST_TO_PROCESS:
        usts = re.findall(ust, elem[1])
        others = re.sub(ust, 'SEP', elem[1]).split('SEP')
        TO_PROCESS.append((elem[0], '?', re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[0])))
        for i, a in enumerate(usts):
            f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=a[7]), '', a[0])
            while f != 'ust.':
                f = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', f)
                f = re.findall(ust, f)[0]
                TO_PROCESS.append((elem[0], 'UST', f[7]))
                f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=f[7]), '', f[0])
            other = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[i + 1])
            if other != '':
                TO_PROCESS.append((elem[0], 'UST+', a[7], other))
            else:
                TO_PROCESS.append((elem[0], 'UST', a[7]))

    PKT_TO_PROCESS = []
    for elem in TO_PROCESS:
        if elem[1] == '?' and elem[2] == '':
            continue
        elif elem[1] == 'UST':
            key = elem[2]
            pref = 'UST '
            if elem[0] != '?':
                pref = 'ART ' + elem[0][1] + ' ' + pref

            if len(key.split('-')) == 1:
                COUNTER[pref + key] = COUNTER.get(pref + key, 0) + 1
            else:
                for i in range(int(key.split('-')[0]), int(key.split('-')[1]) + 1):
                    COUNTER[pref + str(i)] = COUNTER.get(pref + str(i), 0) + 1
        elif elem[1] == 'UST+':
            PKT_TO_PROCESS.append((elem[0], ('UST', elem[2]), elem[3]))
        elif elem[1] == '?':
            PKT_TO_PROCESS.append(elem)

    TO_PROCESS = []
    for elem in PKT_TO_PROCESS:
        pkts = re.findall(pkt, elem[2])
        others = re.sub(pkt, 'SEP', elem[2]).split('SEP')
        TO_PROCESS.append((elem[0], elem[1], '?', re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[0])))
        for i, a in enumerate(pkts):
            f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=a[6]), '', a[0])
            while f != 'pkt':
                f = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', f)
                f = re.findall(pkt, f)[0]
                TO_PROCESS.append((elem[0], elem[1], 'PKT', f[6]))
                f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=f[6]), '', f[0])
            other = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[i + 1])
            if other != '':
                TO_PROCESS.append((elem[0], elem[1], 'PKT+', a[6], other))
            else:
                TO_PROCESS.append((elem[0], elem[1], 'PKT', a[6]))

    LIT_TO_PROCESS = []
    for elem in TO_PROCESS:
        if elem[2] == '?' and elem[3] == '':
            continue
        elif elem[2] == 'PKT':
            key = elem[3]
            pref = 'PKT '
            if elem[1] != '?':
                pref = 'UST ' + elem[1][1] + ' ' + pref
            if elem[0] != '?':
                pref = 'ART ' + elem[0][1] + ' ' + pref

            if len(key.split('-')) == 1:
                COUNTER[pref + key] = COUNTER.get(pref + key, 0) + 1
            else:
                for i in range(int(key.split('-')[0]), int(key.split('-')[1]) + 1):
                    COUNTER[pref + str(i)] = COUNTER.get(pref + str(i), 0) + 1
        elif elem[2] == 'PKT+':
            LIT_TO_PROCESS.append((elem[0], elem[1], ('PKT', elem[3]), elem[4]))
        elif elem[2] == '?':
            LIT_TO_PROCESS.append(elem)

    TO_PROCESS = []
    for elem in LIT_TO_PROCESS:
        lits = re.findall(lit, elem[3])
        others = re.sub(lit, 'SEP', elem[3]).split('SEP')
        TO_PROCESS.append((elem[0], elem[1], elem[2], '?', re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[0])))
        for i, a in enumerate(lits):
            f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=a[6]), '', a[0])
            while f != 'lit.':
                f = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', f)
                f = re.findall(lit, f)[0]
                TO_PROCESS.append((elem[0], elem[1], elem[2], 'LIT', f[6]))
                f = re.sub(r'{LAST}((lub|i|,|oraz)(\s*(w|z))?)?$'.format(LAST=f[6]), '', f[0])
            other = re.sub(r'(lub|i|,|oraz)(\s*(w|z))?$', '', others[i + 1])
            if other != '':
                TO_PROCESS.append((elem[0], elem[1], elem[2], 'LIT+', a[6], other))
            else:
                TO_PROCESS.append((elem[0], elem[1], elem[2], 'LIT', a[6]))

    LAST_TO_PROCESS = []
    for elem in TO_PROCESS:
        if elem[3] == '?' and elem[4] == '':
            continue
        elif elem[3] == 'LIT':
            key = elem[4]
            pref = 'LIT '
            if elem[2] != '?':
                pref = 'PKT ' + elem[2][1] + ' ' + pref
            if elem[1] != '?':
                pref = 'UST ' + elem[1][1] + ' ' + pref
            if elem[0] != '?':
                pref = 'ART ' + elem[0][1] + ' ' + pref

            if len(key.split('-')) == 1:
                COUNTER[pref + key] = COUNTER.get(pref + key, 0) + 1
            else:
                for i in range(ord(key.split('-')[0][0]), ord(key.split('-')[1][0]) + 1):
                    COUNTER[pref + chr(i)] = COUNTER.get(pref + chr(i), 0) + 1
        elif elem[3] == 'LIT+':
            LAST_TO_PROCESS.append((elem[0], elem[1], elem[2], ('LIT', elem[4]), elem[5]))
        elif elem[3] == '?':
            LAST_TO_PROCESS.append(elem)

    return COUNTER


for filename in glob.glob("../ustawy/*.txt"):
    d = for_one(filename)
    sort = sorted(d.items(), key=lambda x: x[1], reverse=True)
    print(filename, sort)
