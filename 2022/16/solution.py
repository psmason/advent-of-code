#!/usr/bin/env python3

import fileinput
from collections import defaultdict
import re
from itertools import chain, combinations

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

_TUNNELS_RE = re.compile("tunnel[s]? lead[s]? to valve[s]? ([A-Z ,]+)$")
_PRESSURE_RE = re.compile("has flow rate=([0-9]+);")

def build_graph(lines):
    g = defaultdict(list)

    for line in lines:
        current_valve = line[6:8]

        tunnels = _TUNNELS_RE.findall(line)
        tunnels = [tunnel.strip() for tunnel in tunnels[0].split(',')]
        for tunnel in tunnels:
            g[current_valve].append(tunnel)

    return g

def all_pairs_shortest_path(g):
    # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    vertices = list(g.keys())
    
    result = {}
    for v in vertices:
        result[v] = {}
        for x in vertices:
            result[v][x] = 9999
            
    for v in vertices:
        result[v][v] = 0

        for e in g[v]:
            result[v][e] = 1

    for k in range(len(vertices)):
        for i in range(len(vertices)):
            for j in range(len(vertices)):
                v_i, v_j, v_k = vertices[i], vertices[j], vertices[k]

                d = result[v_i][v_k] + result[v_k][v_j]
                result[v_i][v_j] = min(result[v_i][v_j], d)
    
    return result

def build_valve_pressures(lines):
    result = {}
    for line in lines:
        current_valve = line[6:8]
        pressure = _PRESSURE_RE.findall(line)
        result[current_valve] = int(pressure[0])
    return result
        

def find_max_pressure(current_location, g, shortest_paths, unvisited_valves, valve_pressures, current_time, time_limit):
    max_pressure_released = -1
    
    for valve in unvisited_valves:
        d = shortest_paths[current_location][valve]

        new_time = current_time
        
        # getting to the valve
        new_time += d
        # opening the valve
        new_time += 1
    
        if current_time <= time_limit:
            pressure_released = valve_pressures[valve]*(time_limit-new_time+1)
            later_steps = find_max_pressure(valve,g,shortest_paths,unvisited_valves-set([valve]),valve_pressures,new_time,time_limit)
            if later_steps > 0:
                pressure_released += later_steps
                
            max_pressure_released = max(max_pressure_released, pressure_released)
    return max_pressure_released
    
# Part 1
lines = get_input()
g = build_graph(lines)
valve_pressures = build_valve_pressures(lines)
shortest_paths = all_pairs_shortest_path(g)
valves_to_visit = set([k for k in valve_pressures.keys() if valve_pressures[k] > 0])
print(find_max_pressure('AA', g, shortest_paths, valves_to_visit, valve_pressures, 1, 30))

# Part 2
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

max_pressure = -1
count = 0
for p in powerset(valves_to_visit):
    if count % 100 == 0:
        print(count)
    count += 1
    my_share = set(p)
    helper_share = valves_to_visit - my_share

    my_pressure = find_max_pressure('AA', g, shortest_paths, my_share, valve_pressures, 1, 26)
    helper_pressure = find_max_pressure('AA', g, shortest_paths, helper_share, valve_pressures, 1, 26)

    max_pressure = max(max_pressure, my_pressure+helper_pressure)
print(max_pressure)
