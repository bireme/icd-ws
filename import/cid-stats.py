#!/usr/bin/env python
# coding: utf-8

import csv
import collections

total_records = 0

keys = 'seq level rec_type table code alt_code cr_ast descr note1 note2'
Entry = collections.namedtuple('Entry', keys)

class OutOfSequence(StandardError):
    '''The record sequence number does not match the record position'''

level_xlate = {'Cap\xc3\xadtulo':'chapter', 'Grupo':'group',
               'Categoria':'category', 'Subcategoria':'subcategory'}

levels = {}
types = set()

with open('../../data/cid10/CID10-matriz.csv') as f:
    for lin in csv.reader(f):
        entry = Entry._make(lin)
        if entry.seq == 'Seq':
            continue # skip header
        elif entry.code == 'ZZZ.Z':
            break # end marker
        total_records += 1
        assert int(entry.seq) == total_records
        level = level_xlate[entry.level]
        levels[level] = levels.get(level, 0) + 1
        types.add(entry.rec_type)

print 'records read :', total_records
print 'levels :', levels
print 'types :', types
