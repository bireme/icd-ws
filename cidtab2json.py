#!/usr/bin/env python
# coding: utf-8

"""

Sample record::

    >>> a15_4 = {
    ...    "code": "A15.4",
    ...    "lang": "pt-br",
    ...    "title": "Tuberculose dos gânglios intratorácicos, com confirmação bacteriológica e histológica",
    ...    "level": "subcat",
    ...    "inclusions": ["Tuberculose ganglionar:", "- hilar", "- mediastinal", "- traqueobrônquica"],
    ...    "inc_notes": [{"start":1, "end":4,
    ...                   "col1": ["com confirmação bacteriológica", " e histológica"]}],
    ...    "exclusions": ["Especificada como primária (A15.7)"],
    ...    "seq": 177
    ... }
    >>> a15_4['code']
    'A15.4'

"""

import sys
import json


# Roman numeral conversion by Mark Pilgrim
# see: http://diveintopython.org/unit_testing/stage_5.html

romanNumeralMap = [('M',  1000), ('CM', 900), ('D',  500), ('CD', 400),
                   ('C',  100),  ('XC', 90), ('L',  50), ('XL', 40),
                   ('X',  10), ('IX', 9), ('V',  5), ('IV', 4), ('I',  1)]

def toRoman(n):
    """convert integer to Roman numeral"""
    if not (0 < n < 4000):
        raise ValueError("number out of range (must be 1..3999)")
    if int(n) != n:
        raise ValueError("non-integers can not be converted")
    result = ""
    for numeral, integer in romanNumeralMap:
        while n >= integer:
            result += numeral
            n -= integer
    return result

INFILE = '../data/cid10/CID10-matriz.txt'

with open('../data/cid10/CID10-categorias-puras.txt') as cats:
    pure_cats = set(cats.read().split())

# Seq	Nível	Tipo	Tabela	Código	Código Alt	CrAst	Descrição

levels = {u'Capítulo' : 'chap',
          u'Grupo': 'group',
          u'Categoria': 'cat',
          u'Subcategoria': 'subcat'}

def convert(start=0, stop=sys.maxsize):
    prev_code = prev_level = entry = None
    chap_num = 0
    entries = []
    with open(INFILE) as infile:
        ct_lines = 0
        for lin in infile:
            lin = unicode(lin.strip(), 'cp1252')
            parts = [p.rstrip() for p in lin.split('\t')]
            seq, level, tag, table, code, alt_code, cr_st, descr = parts[:8]
            col1 = parts[8] if len(parts) >= 9 else None
            col2 = parts[9] if len(parts) == 10 else None
            seq = int(seq)
            level = levels[level]
            tag = tag.strip()
            code = code.strip().upper()
            alt_code = alt_code.strip().upper()
            cr_st = cr_st.strip()
            if code != prev_code:
                # start new entry
                assert tag == u'Título', repr(parts)
                if level == 'chap':
                    chap_num += 1
                    chap = toRoman(chap_num)
                if entry is not None:
                    entries.append(entry)
                entry = dict(_id=code, code=code, lang=u'pt-br', title=descr, seq=seq, level=level, chap=chap)
                if alt_code != code:
                    entry['alt_code'] = alt_code
                if cr_st:
                    entry['cr_st'] = cr_st
                    # print chap, code, descr
                # check nested levels: chap -> group -> cat -> subcat
                if prev_level == 'chap':
                    assert level in ['group'], repr(parts)
                elif prev_level == 'group':
                    assert level in ['group', 'cat'], repr(parts)
                elif prev_level == 'cat':
                    assert level in ['cat', 'subcat', 'group'], repr(parts)
                elif prev_level == 'subcat':
                    assert level in ['chap', 'group', 'cat', 'subcat'], repr(parts)
            else: # same code, add to current record
                # tags [u'Exclus\xe3o', u'Inclus\xe3o', u'Nota', u'T\xedtulo', u'CNota']
                if descr:
                    if tag == u'Nota':
                        entry.setdefault('notes',[]).append([descr])
                    elif tag == u'CNota':
                        entry['notes'][-1].append(descr)
                    elif tag == u'Inclusão':
                        entry.setdefault('inclusions',[]).append(descr)
                    elif tag == u'Exclusão':
                        entry.setdefault('exclusions',[]).append(descr)
                    elif tag == u'Título':
                        if code not in pure_cats:
                            TypeError('unexpected repeated code: %r' % parts)
                    else:
                        raise TypeError('unknown tag: %r' % parts)

            prev_code = code
            prev_level = level
            ct_lines += 1

    #print 'ct_lines:', ct_lines
    print json.dumps(dict(docs=entries[start:stop]))

convert()

"""
Notes:

in CID10.xls, code C43 appears as:

2551	Categoria	Título		C43	C43.-		Melanoma maligno da pele
2552	Subcategoria	Inclusão		C43	C43		Os códigos de morfologia classificáveis em M872-M879 com código de comportamento /3
2553	Subcategoria	Exclusão		C43	C43		Melanoma maligno da pele dos órgãos genitais (C51-C52, C60.-, C63.-)

Here we have a Categoria followed immediately by Subcategoria (without a Title) and Inclusão, Exclusão.

That segment continues:

2554	Subcategoria	Título		C43.0	C43.0		Melanoma maligno do lábio
2555	Subcategoria	Exclusão		C43.0	C43.0		Área vermelha (vermelhão) do lábio (C00.0-C00.2)

####

N50.8 contains column 1 content even in lines with no description


"""
