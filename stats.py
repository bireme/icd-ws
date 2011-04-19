#!/usr/bin/env python

import json

with open('fixtures/sample.json') as sample:
    docs = json.load(sample)['docs']

print len(docs), 'records'

if False:
    for r in docs:
        print r['chap'],
        print r['text']['pt-br']['title']
