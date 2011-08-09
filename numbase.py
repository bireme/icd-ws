#!/usr/bin/env python
# coding: utf-8

# this module allows base conversion using arbitrary digits, unlike Python's
# built-in `int` which is limited to digits from 0-9 and A-Z in that order.

import string

# just lowercase numbers and digits
BASE36 = string.digits+string.ascii_lowercase

# no vowels, to avoid forming words;
# no '1l0' to avoid reading mistakes
BASE28 = ''.join(d for d in BASE36 if d not in 'aeiou1l0') 

def reprbase(n, digits=BASE28, width=0):
    '''returns the value `n` in base `len(digits)`, using `digits`'''
    base = len(digits)
    s = []
    while n:
        n, d = divmod(n, base)
        s.insert(0, digits[d])
    if s:    
        res = ''.join(s)
    else:
        res = digits[0]
    if width:
        return res.rjust(width, digits[0])
    else:
        return res
    
def calcbase(s, digits=BASE28):
    '''returns the numeric value of `s` in base `len(digits)`'''
    return sum(digits.index(dig)*len(digits)**pot
               for pot, dig in enumerate(reversed(s)))

if __name__=='__main__':
    print 'Self test with base 28'

    l = range(11)
    l.extend([calcbase(x) for x in ('3zz', '422','4zz','522','zzz','3222')])
    l.extend([27,28,29,28**2-1,28**2,1001,1100,1200,2000])

    for n in sorted(l):
        s = reprbase(n)
        assert n == calcbase(s), '%s != %s' % (n, s)
        print '%11d\t%8s' % (n, s)

    for n in (10**i for i in range(11)):
        s = reprbase(n, width=5)
        assert n == calcbase(s), '%s != %s' % (n, s)
        print '%11d\t%8s' % (n, s)
    
