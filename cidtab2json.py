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
import csv
import collections

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

INFILE = '../data/cid10/CID10-matriz.csv'
END_CODE = 'ZZZ.Z'

with open('../data/cid10/CID10-categorias-puras.txt') as cats:
    pure_cats = set(cats.read().split())

# Seq   Nível   Tipo    Tabela  Código  Código Alt  CrAst   Descrição

levels = {'Capítulo' : 'chap',
          'Grupo': 'group',
          'Categoria': 'cat',
          'Subcategoria': 'subcat'}

#       seq, level, tag, table, code, alt_code, cr_st, descr = parts[:8]
keys = 'seq level tag table code alt_code cr_st descr note1 note2'
Entry = collections.namedtuple('Entry', keys)

def make_selector():
    flags = set()
    def selector(entry, chap):
        pt_text = entry['text']['pt-br']
        return any([
            entry['level'] == 'chap', # inicios dos capitulos
            entry['chap'] != chap, # ultimo do capítulo
            len(pt_text.get('notes',[])) > 3, # várias notas
            'cr_st' in entry
        ])
    return selector

def convert(start=0, stop=sys.maxsize):
    prev_code = prev_level = entry = None
    chap_num = 0
    entries = []
    selector = make_selector()
    with open(INFILE) as infile:
        ct_lines = 0
        for lin in csv.reader(infile):
            row = Entry._make(lin)
            if row.seq == 'Seq':
                continue # skip header
            seq = int(row.seq)
            level = levels[row.level]
            tag = row.tag.strip()
            code = row.code.strip().upper()
            alt_code = row.alt_code.strip().upper()
            cr_st = row.cr_st.strip()
            if code != prev_code:
                # start new entry
                assert tag == 'Título', entry
                if level == 'chap' or code == END_CODE:
                    chap_num += 1
                    chap = toRoman(chap_num)
                if entry is not None:
                    if selector(entry, chap):
                        entries.append(entry)
                if code == END_CODE: break
                entry = dict(_id=seq, code=code, chap=chap, level=level, seq=seq)
                entry['text'] = {'pt-br':dict(title=row.descr)}
                pt_text = entry['text']['pt-br']
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
                if row.descr:
                    if tag == 'Nota':
                        # there are no records with multiple notes
                        pt_text.setdefault('notes',[]).append(row.descr)
                        assert len(pt_text['notes']) == 1
                    elif tag == 'CNota':
                        # but a note can have multiple continuations
                        pt_text['notes'].append(row.descr)
                    elif tag == 'Inclusão':
                        pt_text.setdefault('inclusions',[]).append(row.descr)
                    elif tag == 'Exclusão':
                        pt_text.setdefault('exclusions',[]).append(row.descr)
                    elif tag == 'Título':
                        if code not in pure_cats:
                            TypeError('unexpected repeated code: %r' % (row,))
                    else:
                        raise TypeError('unknown tag: %r' % (row,))

            prev_code = code
            prev_level = level
            ct_lines += 1

    print json.dumps(dict(docs=entries[start:stop]))

convert()

"""
Notes:

in CID10.xls, code C43 appears as:

2551    Categoria   Título      C43 C43.-       Melanoma maligno da pele
2552    Subcategoria    Inclusão        C43 C43     Os códigos de morfologia classificáveis em M872-M879 com código de comportamento /3
2553    Subcategoria    Exclusão        C43 C43     Melanoma maligno da pele dos órgãos genitais (C51-C52, C60.-, C63.-)

Here we have a Categoria followed immediately by Subcategoria (without a Title) and Inclusão, Exclusão.

That segment continues:

2554    Subcategoria    Título      C43.0   C43.0       Melanoma maligno do lábio
2555    Subcategoria    Exclusão        C43.0   C43.0       Área vermelha (vermelhão) do lábio (C00.0-C00.2)

####

N50.8 contains column 1 content even in lines with no description


"""
