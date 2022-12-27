#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines



_REGISTER_X = 1
_CYCLE = 1
_CYCLES_TO_CHECK = set([20, 60, 100, 140, 180, 220])

def maybe_print_signal_strength():
    if _CYCLE in _CYCLES_TO_CHECK:
        print(_CYCLE * _REGISTER_X, _CYCLE)   

for line in get_input():
    if line == 'noop':
        _CYCLE += 1
        maybe_print_signal_strength()
    else:
        addx = int(line.split(' ')[1])
        _CYCLE += 1
        maybe_print_signal_strength()
        _CYCLE += 1
        _REGISTER_X += addx
        maybe_print_signal_strength()

# Part 2
_CRT = [['.']*40 for i in range(6)]
_CRT_POSITION = 0
_SPRITE_LOCATION = 1

def update_crt():
    row = _CRT_POSITION // 40
    col = _CRT_POSITION % 40
    if abs(_SPRITE_LOCATION - col) <= 1:
        _CRT[row][col] = '#'

def print_crt():
    print('\n'.join([''.join(row) for row in _CRT]))

for line in get_input():
    if line == 'noop':
        update_crt()
        _CRT_POSITION += 1
    else:
        addx = int(line.split(' ')[1])
        update_crt()
        _CRT_POSITION += 1
        update_crt()
        _CRT_POSITION += 1
        _SPRITE_LOCATION += addx
print_crt()
