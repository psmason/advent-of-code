#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.rstrip('\n'))
        return lines

_SNAFU_TO_DECIMAL = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}

def convert_from_snafu(snafu):
    result = 0
    a = list(reversed(list(snafu)))
    for i in range(len(a)):
        result += _SNAFU_TO_DECIMAL[a[i]] * (5**i)
    return result

def convert_to_base5(d):
    result = []    
    while d > 0:
        result.append(str(d % 5))
        d = d // 5
    return ''.join(reversed(result))    

def convert_to_snafu(d):
    def snafu_char_convert(i, carry):
        i += carry
        if i == 0:
            return '0', 0
        elif i == 1:
            return '1', 0
        elif i == 2:
            return '2', 0
        elif i == 3:
            return '=', 1
        elif i == 4:
            return '-', 1
        elif i == 5:
            return '0', 1
    
    base5 = convert_to_base5(d)
    result = []

    carry = 0
    for c in reversed(base5):
        converted_c, carry = snafu_char_convert(int(c), carry)
        result.append(converted_c)
    if carry > 0:
        result.append('1')
        
    return ''.join(reversed(result))

"""
print('test conversions from snafu')
print(1, convert_to_snafu(1))
print(2, convert_to_snafu(2))
print(3, convert_to_snafu(3))
print(4, convert_to_snafu(4))
print(5, convert_to_snafu(5))
print(6, convert_to_snafu(6))
print(7, convert_to_snafu(7))
print(8, convert_to_snafu(8))
print(9, convert_to_snafu(9))
print(10, convert_to_snafu(10))
print(15, convert_to_snafu(15))
print(20, convert_to_snafu(20))
print(2022, convert_to_snafu(2022))
print(12345, convert_to_snafu(12345))
print(314159265, convert_to_snafu(314159265))
"""

# Part 1
input_sum = 0
for snafu in get_input():
    input_sum += convert_from_snafu(snafu)
print(input_sum)
print(convert_to_snafu(int(input_sum)))
