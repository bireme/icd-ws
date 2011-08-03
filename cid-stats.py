#!/usr/bin/env python
# coding: utf-8

from sys import maxsize

min = maxsize
max = 0

with open('CID10-matriz.txt') as f:
    for lin in f:
        parts = lin.split('\t')
        l = len(parts)
        if l < min:
            min = l
        if l > max:
            max = l

print min, max

