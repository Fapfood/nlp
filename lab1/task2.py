wym = r'(wymienion(y|a|e|ego|ej|emu|ą|ym|ych|ymi)|wymienieni)\s*w'
okr = r'(określon(y|a|e|ego|ej|emu|ą|ym|ych|ymi)|określeni)\s*w'
zgd = r'zgodn(y|a|e|ego|ej|emu|ą|ym|ych|ymi|i|ie)\s*z'
matcher = r'(w\s*myśl|mowa\s*w|w\s*rozumieniu|na\s*podstawie|{WYM}|{OKR}|{ZGD})'.format(WYM=wym, OKR=okr, ZGD=zgd)
separator = r'\s*(lub|i|-|,|oraz)(\s*(w|z))?'
art = r'(\s*art\.(\s*\d+{SEP})*\s*\d+)'.format(SEP=separator)
ust = r'(\s*(§|ust\.)(\s*\d+{SEP})*\s*\d+)'.format(SEP=separator)
pkt = r'(\s*pkt(\s*\d+{SEP})*\s*\d+)'.format(SEP=separator)
lit = r'(\s*lit\.(\s*\d+{SEP})*\s*\w+)'.format(SEP=separator)
block = r'({ART}|{UST}|{PKT}|{LIT})+'.format(ART=art, UST=ust, PKT=pkt, LIT=lit)
regex = r'{MCH}({BL}{SEP})*{BL}'.format(SEP=separator, BL=block, MCH=matcher)

print(regex)
