#!/usr/bin/env python3

import fileinput
import copy

_HORIZONTAL_LINE = [(0,0), (1,0), (2,0), (3,0)]
_VERTICAL_LINE =   [(0,0), (0,1), (0,2), (0,3)]
_CROSS =           [(1,0), (0,1), (1,1), (2,1), (1,2)]
_BLOCK =           [(0,0), (1,0), (0,1), (1,1)]
_ELBOW =           [(0,0), (1,0), (2,0), (2,1), (2,2)]

_ALL_SHAPES = [_HORIZONTAL_LINE, _CROSS, _ELBOW, _VERTICAL_LINE, _BLOCK]

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def place_at_top(rock, highest_rock):
    result = []
    for atom in rock:
        x,y = atom
        result.append((x+2, y+highest_rock+4))
    return result

def apply_jet(rock, grid, jet_pattern, jet_cycle):
    push = -1
    if jet_pattern[jet_cycle] == '>':
        push = 1

    for atom in rock:
        x,y = atom
        if x+push < 0 or x+push > 6 or grid[y][x+push] == '#':
            return rock
    
    result = []
    for atom in rock:
        x,y = atom
        result.append((x+push, y))
    return result

def fall_one_unit(rock, chamber):
    can_drop = True
    for atom in rock:
        x,y = atom
        if y-1 < 0 or chamber[y-1][x] == '#':
            can_drop = False
            break
    if not can_drop:
        return (False, rock)
    result = []
    for atom in rock:
        x,y = atom
        result.append((x, y-1))
    return (True, result)

def set_at_rest(rock, chamber, highest_rock):
    highest_result = highest_rock
    for atom in rock:
        x,y = atom
        chamber[y][x] = '#'
        highest_result = max(highest_result, y)
    return highest_result

def pretty_print(chamber):
    print('')
    print('\n'.join(reversed([''.join(row) for row in chamber])))

def pretty_print_with_rock(chamber, rock):
    tmp = copy.deepcopy(chamber)
    for atom in rock:
        x,y = atom
        tmp[y][x] = '@'
    print('')
    print('\n'.join(reversed([''.join(row) for row in tmp])))

def forms_seal(rock, chamber, rock_count):
    def _check_two_rows(bottom_row, top_row):
        for col in range(7):
            if bottom_row[col] == '.' and top_row[col] == '.':
                return False
        return True
    
    y_min, y_max = rock[0][1], rock[0][1]
    for atom in rock:
        _,y = atom
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    # A seal can be formed by the combination of two rows, spanning
    # where the rock ended up at rest, and the row above.
    for row in range(y_min, y_max+1):
        bottom_row = chamber[row]
        top_row = chamber[row+1]

        if _check_two_rows(bottom_row, top_row):
            return True, row

    return False, None

def fingerprint_chamber(chamber):
    return hash('\n'.join([''.join(row) for row in chamber]))
        
rock_count = 0
highest_rock = -1
jet_pattern = get_input()[0].strip()
jet_cycle = 0
chamber = [['.']*7 for _ in range(5)]

cycle_captured_height = None
cycle_captured_simulated_height = None
cycle_cache = {}

#rocks_to_drop = 2022
rocks_to_drop = 1000000000000

while True:
    rock_count += 1
    rock_cycle = (rock_count-1) % len(_ALL_SHAPES)
    rock = place_at_top(_ALL_SHAPES[rock_cycle], highest_rock)
    while True:
        #pretty_print_with_rock(chamber, rock)
        rock = apply_jet(rock, chamber, jet_pattern, jet_cycle)
        jet_cycle += 1
        jet_cycle = jet_cycle % len(jet_pattern)

        could_fall, rock = fall_one_unit(rock, chamber)
        if not could_fall:
            highest_rock = set_at_rest(rock, chamber, highest_rock)
            while len(chamber) < highest_rock + 10:
                chamber.append(['.']*7)
            if rock_count > 500:
                creates_seal, seal_floor = forms_seal(rock, chamber, rock_count)
                
                # if a cycle-determined height is already captured, don't let
                # other cycle detections interfere in the result.
                if creates_seal and cycle_captured_simulated_height is None:
                    fingerprint = fingerprint_chamber(chamber[seal_floor:])
                    if (rock_cycle, jet_cycle) in cycle_cache:
                        cached_fingerprint, cached_highest_rock, cached_rock_count = cycle_cache[(rock_cycle, jet_cycle)]
                        if fingerprint == cached_fingerprint:
                            height_delta = highest_rock - cached_highest_rock
                            rock_count_delta = rock_count - cached_rock_count

                            remaining_rocks = rocks_to_drop-rock_count                        
                            print('cycle found', rock_cycle, jet_cycle, rock_count, height_delta, rock_count_delta)

                            cycle_captured_height = highest_rock
                            cycle_captured_simulated_height = highest_rock + height_delta * (remaining_rocks // rock_count_delta)
                            drops_remaining = remaining_rocks % rock_count_delta

                            # Jumps the simulation ahead by however many cycles that fit. 
                            rock_count = rocks_to_drop - drops_remaining
                        
                    cycle_cache[(rock_cycle, jet_cycle)] = (fingerprint, highest_rock, rock_count)
            break    
    if rock_count == rocks_to_drop: 
        break

print(cycle_captured_simulated_height + highest_rock - cycle_captured_height + 1)

        
    
    

