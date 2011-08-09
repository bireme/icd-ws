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

import csv
import collections
import itertools

with open('../data/cid10/CID10-categorias-puras.txt') as cats:
    pure_cats = set(cats.read().split())

levels = {'Capítulo' : 'chap',
          'Grupo': 'group',
          'Categoria': 'cat',
          'Subcategoria': 'subcat'}

types = {'T\xc3\xadtulo' : 'title',
         'Nota' : 'note',
         'CNota' : 'cnote',
         'Inclus\xc3\xa3o' : 'incl',
         'Exclus\xc3\xa3o' : 'excl',
         }
          

# Seq  Nível  Tipo  Tabela  Código  Código Alt  CrAst  Descrição...
#    seq level type table code alt_code cr_st descr col1  col2
Row = collections.namedtuple('Row', 
    'seq level type table code alt_code cr_st descr note1 note2')

class InputError(StandardError):
    '''Malformed input file'''

def get_entry_rows(infile):
    END_CODE = 'ZZZ.Z'
    for line_index, lin in enumerate(csv.reader(infile)):
        row = Row._make(lin)
        try:
            level = levels[row.level]
        except KeyError:
            if line_index == 0 or row.level == '':
                # ignore header line and blank lines
                continue
            else:
                raise InputError(line_index+1)
        if row.code == END_CODE:
            return
        row_list = list(row)
        level_pos = row._fields.index('level')
        type_pos = row._fields.index('type')
        row_list[level_pos] = level
        row_list[type_pos] = types[row.type]
        yield Row(*row_list)

def group_id(row):
    return '{0}:{1}'.format(row.code, row.level)

def convert(infile_name):
    level_steps = set()
    type_steps = set()
    prev_level = None
    with open(INFILE) as infile:
        for code, record in itertools.groupby(get_entry_rows(infile), group_id):
            rows = list(record)
            level = rows[0].level
            #if (prev_level, level) == ('group', 'subcat'): 
            #print '{0:8} {1} {0}'.format (code, '-' * 70)
            level_steps.add((prev_level, level))
            prev_level = level
            prev_type = None
            for row in rows:
                if prev_type == None and row.type == 'excl' and row.code not in pure_cats:
                    print ' {0.seq:>5} {0.level:6} {0.type}'.format(row)
                type_steps.add((prev_type, row.type))
                prev_type = row.type
    for i in sorted(level_steps):
        print i
    for i in sorted(type_steps):
        print i

INFILE = '../data/cid10/CID10-matriz.csv'
convert(INFILE)


"""
Notes:

Example of a category title followed immediately by a subcategory exclusion:

2280    Categoria   Título      C13 C13.-       Neoplasia maligna da hipofaringe
2281    Subcategoria    Exclusão        C13 C13     Seio piriforme (C12)


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
