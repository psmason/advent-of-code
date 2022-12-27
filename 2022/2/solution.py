#!/usr/bin/env python3

import fileinput
from collections import defaultdict

_OPPONENT_MOVE = {
    'A': 'ROCK',
    'B': 'PAPER',
    'C': 'SCISSORS',
}

_STRATEGY_MOVE = {
    'X': 'ROCK',
    'Y': 'PAPER',
    'Z': 'SCISSORS',
}

_SCORING = {
    'ROCK': {
        'ROCK'    : 3 + 1,
        'PAPER'   : 6 + 2,
        'SCISSORS': 0 + 3,
    },
    'PAPER': {
        'ROCK'    : 0 + 1,
        'PAPER'   : 3 + 2,
        'SCISSORS': 6 + 3,
    },
    'SCISSORS': {
        'ROCK'    : 6 + 1,
        'PAPER'   : 0 + 2,
        'SCISSORS': 3 + 3,
    },
}

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def score_result(line):
    if not line:
        return 0
    lhs, rhs = line.split(' ')
    return _SCORING[_OPPONENT_MOVE[lhs]][_STRATEGY_MOVE[rhs]]
    

lines = get_input()

# What would your total score be if everything goes exactly according to your strategy guide?
print(sum([score_result(l) for l in lines]))

_STRATEGY_RESULT = {
    'X': 'LOSE',
    'Y': 'DRAW',
    'Z': 'WIN',
}

_SCORING_V2 = {
    'ROCK': {
        'LOSE' : 0 + 3,
        'DRAW' : 3 + 1,
        'WIN'  : 6 + 2,
    },
    'PAPER': {
        'LOSE' : 0 + 1,
        'DRAW' : 3 + 2,
        'WIN'  : 6 + 3,
    },
    'SCISSORS': {
        'LOSE' : 0 + 2,
        'DRAW' : 3 + 3,
        'WIN'  : 6 + 1,
    },
}

def score_result_v2(line):
    if not line:
        return 0
    lhs, rhs = line.split(' ')
    return _SCORING_V2[_OPPONENT_MOVE[lhs]][_STRATEGY_RESULT[rhs]]

# Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?
print(sum([score_result_v2(l) for l in lines]))
