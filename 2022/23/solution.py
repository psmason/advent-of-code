#!/usr/bin/env python3

import fileinput
from collections import defaultdict

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.rstrip('\n'))
        return lines

def find_elves(lines):
    result = set()
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == '#':
                result.add((row, col))
    return result

def pretty_print(elves):
    max_row, max_col = -1, -1
    for elf in elves:
        max_row = max(max_row, elf[0])
        max_col = max(max_col, elf[1])

    grid = [['.']*(max_col+1) for _ in range(max_row+1)]
    for elf in elves:
        grid[elf[0]][elf[1]] = '#'

    print('')
    print('\n'.join([''.join(row) for row in grid]))

_NW = 'NW'
_N  = 'N'
_NE = 'NE'
_E  = 'E'
_SE = 'SE'
_S  = 'S'
_SW = 'SW'
_W  = 'W'

_RULES = [
    (set([_N, _NW, _NE]), _N),
    (set([_S, _SW, _SE]), _S),
    (set([_W, _NW, _SW]), _W),
    (set([_E, _NE, _SE]), _E),
]

def find_surrounding_elves(elf, elves):
    result = set()

    row, col = elf
    locations_to_check = [
        ((row-1, col-1), _NW),
        ((row-1, col),   _N),
        ((row-1, col+1), _NE),
        ((row,   col+1), _E),
        ((row+1, col+1), _SE),
        ((row+1, col),   _S),
        ((row+1, col-1), _SW),
        ((row,   col-1), _W),
    ]
    for location, direction in locations_to_check:
        if location in elves:
            result.add(direction)
            
    return result

def check_rule(surrounding_elves, rule):
    positions_to_check, direction = rule
    for position in positions_to_check:
        if position in surrounding_elves:
            return None
    return direction

def apply_move(elf, direction):
    row, col = elf
    if direction == _N:
        return (row-1, col)
    elif direction == _E:
        return (row, col+1)
    elif direction == _S:
        return (row+1, col)
    elif direction == _W:
        return (row, col-1)
    else:
        raise Exception('unexpected direction', direction)

def make_proposal_move(elf, surrounding_elves, direction_offset):
    if len(surrounding_elves) == 0:
        return elf
    
    for i in range(4):
        rule_offset = (direction_offset + i) % len(_RULES)
        check_result = check_rule(surrounding_elves, _RULES[rule_offset])
        if check_result is not None:
            return apply_move(elf, check_result)

    # No rule is satisfied
    return elf

def conduct_round(elves, direction_offset):
    result = set()
    
    # First half
    proposals = defaultdict(list)
    for elf in elves:
        surrounding_elves = find_surrounding_elves(elf, elves)
        proposal_move = make_proposal_move(elf, surrounding_elves, direction_offset)
        proposals[proposal_move].append(elf)

    # Second half
    for proposal, elves_for_proposal in proposals.items():
        if len(elves_for_proposal) == 1:
            result.add(proposal)
        else:
            for colliding_elf in elves_for_proposal:
                result.add(colliding_elf)
            
    return result

def calculate_bounding_rectangle(elves):
    min_row, min_col = 999999, 999999
    max_row, max_col = -1, -1
    for elf in elves:
        min_row = min(min_row, elf[0])
        max_row = max(max_row, elf[0])
        min_col = min(min_col, elf[1])
        max_col = max(max_col, elf[1])

    return (max_row-min_row+1) * (max_col-min_col+1) - len(elves)

# Part 1
elves = find_elves(get_input())
rounds = 10
for i in range(10):
    elves = conduct_round(elves, i)
print(calculate_bounding_rectangle(elves))

# Part 2
elves = find_elves(get_input())
current_round = 0
while True:
    updated_elves = conduct_round(elves, current_round)
    if len(updated_elves - elves) == 0:
        break
    current_round += 1
    elves = updated_elves

print(current_round+1)
    
    
