#!/usr/bin/env python3

import fileinput
from collections import deque

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def get_cubes(lines):
    cubes = []
    for line in lines:
        x,y,z = line.split(',')
        x,y,z = int(x), int(y), int(z)

        cubes.append((x,y,z))
    return cubes

def find_surface_area(cubes):
    surface_area = 0
    
    placements = set()
    for cube in cubes:
        x,y,z = cube

        if (x,y,z) in placements:
            raise Exception('duplicate found')

        surface_area += 6
        if (x+1,y,z) in placements:
            surface_area -= 2
        if (x-1,y,z) in placements:
            surface_area -= 2
        if (x,y+1,z) in placements:
            surface_area -= 2
        if (x,y-1,z) in placements:
            surface_area -= 2
        if (x,y,z+1) in placements:
            surface_area -= 2
        if (x,y,z-1) in placements:
            surface_area -= 2
            
        placements.add((x,y,z))
    return surface_area

# Part 1
cubes = get_cubes(get_input())
print(find_surface_area(cubes))

# Part 2
def find_ranges(cubes):
    x_min, x_max = 9999, -9999
    y_min, y_max = 9999, -9999
    z_min, z_max = 9999, -9999

    for cube in cubes:
        x, y, z = cube
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
        z_min = min(z_min, z)
        z_max = max(z_max, z)

    return x_min, x_max, y_min, y_max, z_min, z_max
x_min, x_max, y_min, y_max, z_min, z_max = find_ranges(get_cubes(get_input()))
print(find_ranges(cubes))

# build a complement cube
complement_cubes = set()
for x in range(x_min-1, x_max+2):
    for y in range(y_min-1, y_max+2):
        for z in range(z_min-1, z_max+2):
            complement_cubes.add((x,y,z))
for cube in cubes:
    complement_cubes.remove(cube)

def find_reachable_cubes(cubes, start):
    def maybe_enqueue(candidate):
        if candidate in cubes and candidate not in visited:
            visit_queue.append(candidate)
            visited.add(candidate)
    
    visited = set()
    visited.add(start)

    visit_queue = deque()
    visit_queue.append(start)

    while len(visit_queue) > 0:
        current_cube = visit_queue.popleft()
        x, y, z = current_cube
        
        maybe_enqueue((x+1,y,z))
        maybe_enqueue((x-1,y,z))
        maybe_enqueue((x,y+1,z))
        maybe_enqueue((x,y-1,z))
        maybe_enqueue((x,y,z+1))
        maybe_enqueue((x,y,z-1))

    return visited

exterior_cubes = find_reachable_cubes(complement_cubes, (x_min, y_min, z_min))
for cube in exterior_cubes:
    complement_cubes.remove(cube)
print(find_surface_area(cubes) - find_surface_area(complement_cubes))  



