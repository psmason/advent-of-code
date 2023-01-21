#!/usr/bin/env python3

import fileinput
import copy
from collections import defaultdict
from collections import deque

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.rstrip('\n'))
        return lines

def build_grid(lines):
    rows = len(lines)-2
    cols = len(lines[0])-2
    return [['.']*cols for _ in range(rows)]

def pretty_print(grid, blizzards):
    tmp = copy.deepcopy(grid)

    for location, symbols in blizzards.items():
        row, col = location
        if len(symbols) == 1:
            tmp[row][col] = next(iter(symbols))
        else:
            tmp[row][col] = str(len(symbols))

    rows, cols = len(tmp), len(tmp[0])
    tmp = [['.'] + ['#']*(cols-1)] + tmp
    tmp = tmp + [['#']*(cols-1) + ['.']]
        
    print('\n'.join([''.join(row) for row in tmp]))
    print('')

_UP    = '^'
_DOWN  = 'v'
_LEFT  = '<'
_RIGHT = '>'
        
def find_blizzards(lines):
    result = defaultdict(set)
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] in [_UP, _DOWN, _LEFT, _RIGHT]:
                result[(row-1, col-1)].add(lines[row][col])
    return result

_BLIZZARDS_CACHE = {}
def increment_blizzards(grid, blizzards, minutes):
    if minutes in _BLIZZARDS_CACHE:
        return _BLIZZARDS_CACHE[minutes]
    
    result = defaultdict(set)
    rows, cols = len(grid), len(grid[0])
    for location, blizzards_at_location in blizzards.items():
        for symbol in blizzards_at_location:
            row, col = location
            if symbol == _UP:
                row -= minutes
            elif symbol == _DOWN:
                row += minutes
            elif symbol == _LEFT:
                col -= minutes
            elif symbol == _RIGHT:
                col += minutes
            row = row % rows
            col = col % cols
            result[(row, col)].add(symbol)
    
    _BLIZZARDS_CACHE[minutes] = result
    return result 

_FINGERPRINTS_CACHE = {}
def fingerprint(blizzards, minutes):
    if minutes in _FINGERPRINTS_CACHE:
        return _FINGERPRINTS_CACHE[minutes]
    _FINGERPRINTS_CACHE[minutes] = hash(str(blizzards))
    return _FINGERPRINTS_CACHE[minutes]

def candidate_moves(grid, location, blizzards, minute):
    new_blizzards = increment_blizzards(grid, blizzards, minute+1)

    result = []
    if location == (-1, 0):
        # Wait at the beginning
        result.append(location)
        if (0,0) not in new_blizzards:
            # Move into the grid
            result.append((0,0))
        return result

    rows, cols = len(grid), len(grid[0])
    row, col = location
    for candidate in [
            (row-1, col),   # up
            (row+1, col),   # down
            (row,   col-1), # left
            (row,   col+1), # right
            (row,   col),   # wait
    ]:
        if candidate in [(-1, 0), (rows, cols-1)]:
            # Always safe locations
            result.append(candidate)
        else:
            candidate_row, candidate_col = candidate
            if candidate_row < 0:
                continue
            if candidate_row >= rows:
                continue
            if candidate_col < 0:
                continue
            if candidate_col >= cols:
                continue

            if candidate in new_blizzards:
                continue
            result.append(candidate)
            
    return result
        
def traverse(grid, blizzards, minute, start, finish):
    location = start
    visit_queue = deque()
    visit_queue.append((location, minute))
    visited = set()
    rows, cols = len(grid), len(grid[0])

    visited.add((location, fingerprint(blizzards, minute)))
    
    while len(visit_queue) > 0:
        location, minute = visit_queue.popleft()
        if location == finish:
            # The exit has been found
            return minute
        
        current_blizzards = increment_blizzards(grid, blizzards, minute)
        
        candidates = candidate_moves(grid, location, blizzards, minute)
        upcoming_blizzards_fingerprint = fingerprint(increment_blizzards(grid, blizzards, minute+1), minute+1)
        for candidate in candidates:
            if (candidate, upcoming_blizzards_fingerprint) not in visited:
                visit_queue.append((candidate, minute+1))
                # There's no need to revisit a location if the blizzard fingerprint is identical
                visited.add((candidate, upcoming_blizzards_fingerprint))

# Part 1
lines = get_input()
grid = build_grid(lines)
rows, cols = len(grid), len(grid[0])
blizzards = find_blizzards(lines)
print(traverse(grid, blizzards, 0, (-1, 0), (rows, cols-1)))

# Part 2
first_crossing = traverse(grid, blizzards, 0, (-1, 0), (rows, cols-1))
print('first crossing', first_crossing)
second_crossing = traverse(grid, blizzards, first_crossing, (rows, cols-1), (-1, 0))
print('second crossing', second_crossing)
third_crossing = traverse(grid, blizzards, second_crossing, (-1, 0), (rows, cols-1))
print('third crossing', third_crossing)
