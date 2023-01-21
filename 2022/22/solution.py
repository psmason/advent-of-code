#!/usr/bin/env python3

import copy
import fileinput
import re

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.rstrip('\n'))
        return lines

def parse_moves(line):
    get_move_count = re.compile('^[0-9]+')

    s = line
    result = []
    direction = 0
    while len(s) > 0:
        moves = get_move_count.findall(s)[0]        
        result.append((direction, int(moves)))

        if len(s) == len(moves):
            return result
        direction = s[len(moves)]
        s = s[len(moves)+1:]

    return result

def build_grid(lines):
    # Add an extra row and column so that boundaries become
    # wraparound cases. 
    rows = len(lines)+2
    cols = max([len(line) for line in lines])+2
    grid = [[' ']*cols for row in range(rows)]
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            grid[row+1][col+1] = lines[row][col]
    return grid

def pretty_print_grid(grid, location):
    tmp = copy.deepcopy(grid)
    if location is not None:
        row, col = location
        tmp[row][col] = 'O'
    print('\n'.join([''.join(row) for row in tmp]))

def apply_move(grid, location, orientation, moves, warp_table):
    def update_location(location, orientation):
        row, col = location
        if orientation == 0:
            col += 1
        elif orientation == 180:
            col -= 1
        elif orientation == 90:
            row -= 1
        elif orientation == 270:
            row += 1
        else:
            raise Exception("unexpected orientation", orientation)

        row = row % len(grid)
        col = col % len(grid[row])
        return (row, col)

    def maybe_wrap_location(location, orientation):
        original_location = location
        original_orientation = orientation
        row, col = location

        if warp_table[row][col] is not None:
            row, col, orientation = warp_table[row][col]
        

        while grid[row][col] not in ['.', '#']:
            row, col = update_location((row, col), orientation)
        if grid[row][col] == '.':
            return (row, col), orientation
        else:
            return update_location(original_location, (original_orientation+180)%360), original_orientation

    row, col = location
    for i in range(moves):
        proposed_location = update_location(location, orientation)
        proposed_row, proposed_col = proposed_location
        if grid[proposed_row][proposed_col] == '#':
            break
        location = proposed_location
        location, orientation = maybe_wrap_location(location, orientation)
    return location, orientation

def find_start(grid):
    for col in range(len(grid[1])):
        if grid[1][col] == '.':
            return (1, col)

def apply_rotation(orientation, rotation):
    if rotation == 'R':
        return (orientation-90) % 360
    elif rotation == 'L':
        return (orientation+90) % 360
    else:
        # Assume zero rotation
        return orientation

def get_orientation_score(orientation):
    if orientation == 0:
        return 0
    elif orientation == 270:
        return 1
    elif orientation == 180:
        return 2
    elif orientation == 90:
        return 3
    raise Exception("unexpected orientation for scoring", orientation)

def build_empty_warp_table(grid):
    rows = len(grid)
    cols = len(grid[0])
    return [[None]*cols for row in range(rows)]

lines = get_input()
moves = parse_moves(lines[-1])
grid = build_grid(lines[:-2])
warp_table = build_empty_warp_table(grid)

# Part 1
location = find_start(grid)
orientation = 0
for move in moves:
    rotation, shift_amount = move
    orientation = apply_rotation(orientation, rotation)
    location, orientation = apply_move(grid, location, orientation, shift_amount, warp_table)

print(1000*(location[0])+4*(location[1])+get_orientation_score(orientation))


# Part 2
def build_warp_table(cube_edge_length):
    """
    From the example. The actual input is a different cube layout of edge size 50.

            1111
            1111
            1111
            1111
    222233334444
    222233334444
    222233334444
    222233334444
            55556666
            55556666
            55556666
            55556666
    """
    rows = cube_edge_length * 4
    # Padding the grid for wrap events
    rows += 2

    cols = cube_edge_length * 3
    cols += 2

    warp_grid = [[None]*cols for row in range(rows)]

    # each element is a tuple:
    # * destination row
    # * destination col
    # * destination orientation

    for i in range(cube_edge_length):
        warp_grid[0][cube_edge_length+1+i]                      = (3*cube_edge_length+1+i, 1,                      0)
        warp_grid[0][2*cube_edge_length+1+i]                    = (4*cube_edge_length,     1+i,                    90)
        warp_grid[1+i][3*cube_edge_length+1]                    = (3*cube_edge_length-i,   2*cube_edge_length,     180)
        warp_grid[cube_edge_length+1][2*cube_edge_length+1+i]   = (cube_edge_length+1+i,   2*cube_edge_length,     180)
        warp_grid[cube_edge_length+1+i][2*cube_edge_length+1]   = (cube_edge_length,       2*cube_edge_length+1+i, 90)
        warp_grid[2*cube_edge_length+1+i][2*cube_edge_length+1] = (cube_edge_length-i,     3*cube_edge_length,     180)
        warp_grid[3*cube_edge_length+1][cube_edge_length+1+i]   = (3*cube_edge_length+1+i, cube_edge_length,       180)
        warp_grid[3*cube_edge_length+1+i][cube_edge_length+1]   = (3*cube_edge_length,     cube_edge_length+1+i,   90)
        warp_grid[4*cube_edge_length+1][1+i]                    = (1,                      2*cube_edge_length+1+i, 270)
        warp_grid[3*cube_edge_length+1+i][0]                    = (1,                      cube_edge_length+1+i,   270)
        warp_grid[2*cube_edge_length+1+i][0]                    = (cube_edge_length-i,     cube_edge_length+1,     0)
        warp_grid[2*cube_edge_length][1+i]                      = (cube_edge_length+1+i,   cube_edge_length+1,     0)
        warp_grid[cube_edge_length+1+i][cube_edge_length]       = (2*cube_edge_length+1,   1+i,                    270)
        warp_grid[1+i][cube_edge_length]                        = (3*cube_edge_length-i,   1,                      0)
    return warp_grid

warp_table = build_warp_table(50)

location = find_start(grid)
orientation = 0
for move in moves:
    rotation, shift_amount = move
    orientation = apply_rotation(orientation, rotation)
    location, orientation = apply_move(grid, location, orientation, shift_amount, warp_table)

print(1000*(location[0])+4*(location[1])+get_orientation_score(orientation))

