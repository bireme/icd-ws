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
