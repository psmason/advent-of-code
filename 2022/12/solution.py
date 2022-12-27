#!/usr/bin/env python3

import fileinput
from collections import deque

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def build_grid(lines):
    rows = len(lines)
    cols = len(lines[0])
    grid = [[None]*cols for _ in range(rows)]
    start = (-1, -1)
    for row in range(rows):
        for col in range(cols):
            grid[row][col] = lines[row][col]
            if lines[row][col] == 'S':
                start = (row, col)
    return grid, start

def candidate_steps(grid, loc):
    def height_difference(l1, l2):
        c1 = grid[l1[0]][l1[1]]
        if c1 == 'S':
            c1 = 'a'
        elif c1 == 'E':
            c1 = 'z'
            
        c2 = grid[l2[0]][l2[1]]
        if c2 == 'S':
            c2 = 'a'
        elif c2 == 'E':
            c2 = 'z'
            
        return ord(c2) - ord(c1)

    def valid_row(grid, row):
        return row >= 0 and row < len(grid)

    def valid_col(grid, col):
        return col >= 0 and col < len(grid[0])

    row, col = loc
    candidates = [
        (row-1, col),
        (row+1, col),
        (row, col-1),
        (row, col+1),
    ]

    result = []
    for candidate in candidates:
        if valid_row(grid, candidate[0]) and valid_col(grid, candidate[1]):
            if height_difference(loc, candidate) <= 1:
                result.append(candidate)
    return result

def shortest_path(grid, start):
    visit_queue = deque()
    visit_queue.append((start, 0))

    already_queued = set()
    already_queued.add(start)
    
    while True:
        if len(visit_queue) == 0:
            # Traversal exhausted, so just return -1 for impossible.
            return -1
        
        current_location = visit_queue.popleft()
        c = grid[current_location[0][0]][current_location[0][1]]
        if c == 'E':
            return current_location[1]
    
        for candidate in candidate_steps(grid, current_location[0]):
            if candidate not in already_queued:
                visit_queue.append((candidate, current_location[1]+1))
                already_queued.add(candidate)

# Part 1
lines = get_input()
grid, start = build_grid(lines)
print(shortest_path(grid, start))

# Part 2
def find_candidate_starts(grid):
    rows = len(grid)
    cols = len(grid[0])

    result = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] in ['S', 'a']:
                result.append((row, col))
    return result
paths = [shortest_path(grid, start) for start in find_candidate_starts(grid)]
paths = [path for path in paths if path > 0]
print(sorted(paths)[0])
            

