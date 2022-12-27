#!/usr/bin/env python3

import copy
import fileinput
import math
import re
from collections import defaultdict

_ROBOT_LIMIT = 10
_ORE      = 0
_CLAY     = 1
_OBSIDIAN = 2
_GEODE    = 3

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def parse_blueprint(line):
    ore_re = re.compile("Each ore robot costs ([0-9]+) ore.")
    ore_robot_cost = (int(ore_re.findall(line)[0]), 0, 0)

    clay_re = re.compile("Each clay robot costs ([0-9]+) ore.")
    clay_robot_cost = (int(clay_re.findall(line)[0]), 0, 0)

    obsidian_re = re.compile("Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay.")
    obsidian_robot_cost = obsidian_re.findall(line)
    obsidian_robot_cost = (int(obsidian_robot_cost[0][0]), int(obsidian_robot_cost[0][1]), 0)

    geode_re = re.compile("Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.")
    geode_robot_cost = geode_re.findall(line)
    geode_robot_cost = (int(geode_robot_cost[0][0]), 0, int(geode_robot_cost[0][1]))

    return {
        "ORE"     : ore_robot_cost,
        "CLAY"    : clay_robot_cost,
        "OBSIDIAN": obsidian_robot_cost,
        "GEODE"   : geode_robot_cost
    }   

def pretty_print_build_options(search_table, robots):
    print([t for t in search_table[robots].items() if len(t[1])>0])

def build_geodes_table(robot_costs, time_limit):
    def compute_new_resource_tuple(starting_resources, robots, time_delta, robot_cost):
        result = list(starting_resources)
        for r in [_ORE, _CLAY, _OBSIDIAN, _GEODE]:
            result[r] += robots[r]*time_delta
        # Deducting however much the robot cost.
        for r in [_ORE, _CLAY, _OBSIDIAN]:
            result[r] -= robot_cost[r]
        return tuple(result)

    def compute_time_for_resources(starting_resources, available_robots, robot_cost):
        max_time_needed = -1
        for i in range(len(robot_cost)):
            if robot_cost[i] == 0:
                continue
            max_time_needed = max(max_time_needed, math.ceil(max(0, robot_cost[i]-starting_resources[i]) / available_robots[i]))
        return max_time_needed

    def is_strictly_fewer_resources(lhs, rhs):
        for i in range(len(lhs)):
            if lhs[i] > rhs[i]:
                return False
        return True

    def maybe_skip_update(new_time, existing_resource_paths, updated_resources):
        for t in range(1, new_time):
            if updated_resources in search_table[target_tuple][t]:
                return True
            
        for existing_resource_path in existing_resource_paths:
            if is_strictly_fewer_resources(updated_resources, existing_resource_path):
                return True

    def update_search_table(already_built_robots, target_tuple, robot_to_build):
        path_options = search_table[already_built_robots]

        filtering_ts = None
        filtering_resources = None
        
        for timestamp_option in sorted(path_options.keys()):
            time_needed, resource_options = timestamp_option, path_options[timestamp_option]                
            for resources in resource_options:                
                # Time to collect resources
                time_delta = compute_time_for_resources(resources, already_built_robots, robot_costs[robot_to_build])
                # Time to build the robot
                time_delta += 1

                new_time = time_needed + time_delta
                if new_time <= time_limit:
                    updated_resources = compute_new_resource_tuple(resources, already_built_robots, time_delta, robot_costs[robot_to_build])
                    existing_resource_paths = search_table[target_tuple][new_time]
                    if len(existing_resource_paths) == 0:
                        search_table[target_tuple][new_time].add(updated_resources)
                        #print('added')
                        continue

                    if updated_resources in existing_resource_paths:
                        continue

                    search_table[target_tuple][new_time].add(updated_resources)

                    """
                    if maybe_skip_update(new_time, existing_resource_paths, updated_resources):
                        #print('skipped')
                        continue
                    if filtering_ts is None:
                        filtering_ts = new_time
                        filtering_resources = updated_resources
                    else:
                        if new_time > filtering_ts:
                            filtering_resources_option = compute_new_resource_tuple(filtering_resources, target_tuple, max(0, new_time-filtering_ts), (0,0,0))                        
                            if is_strictly_fewer_resources(updated_resources, filtering_resources_option):
                                #print('skipped')
                                continue
                    
                    #print('added')
                    search_table[target_tuple][new_time].add(updated_resources)
                    removals = []
                    for existing_resource_path in existing_resource_paths:
                        if not existing_resource_path == updated_resources:
                            if is_strictly_fewer_resources(existing_resource_path, updated_resources):
                                removals.append(existing_resource_path)
                    for removal in removals:
                        #print('removing', removal, updated_resources, is_strictly_fewer_resources(removal, updated_resources))
                        #print('removing')
                        search_table[target_tuple][new_time].remove(removal)   
                    """     

    def make_build_options(target_tuple):
        result = []
        for i in range(len(target_tuple)):
            option = list(target_tuple)
            option[i] -= 1

            if i == 0 and option[i] == 0:
                # there's always at least one ore robot
                continue

            if i == 2 and option[1] == 0:
                # can't build obsidian without clay robots
                continue

            if i == 3 and option[2] == 0:
                # can't build geode without obsidian robots
                continue

            if option[i] >= 0:
                result.append((tuple(option), i))
        return result
    
    # Table filling exercise.

    # Initialization
    search_table = defaultdict(dict)
    for ore_robots in range(_ROBOT_LIMIT):
        for clay_robots in range(_ROBOT_LIMIT):
            for obsidian_robots in range(_ROBOT_LIMIT):
                for geode_robots in range(_ROBOT_LIMIT):
                    for timestamp in range(1, time_limit+1):                        
                        # Each element of a set of resource tuples
                        search_table[(ore_robots, clay_robots, obsidian_robots, geode_robots)][timestamp] = set()

    search_table[(1,0,0,0)][1].add((0,0,0,0))
    for target_geode_count in range(_ROBOT_LIMIT):
        for target_obsidian_count in range(_ROBOT_LIMIT):
            for target_clay_count in range(_ROBOT_LIMIT):
                for target_ore_count in range(1, _ROBOT_LIMIT):
                    target_tuple = (target_ore_count, target_clay_count, target_obsidian_count, target_geode_count)
                    if target_tuple == (1, 0, 0, 0):
                        continue
            
                    already_built_options = make_build_options(target_tuple)
                    for already_built_robots, robot_to_build in already_built_options:
                        update_search_table(already_built_robots, target_tuple, robot_to_build)
    return search_table

def find_max_geodes(search_table, time_limit):
    max_geodes = 0
    for ore_robots in range(_ROBOT_LIMIT):
        for clay_robots in range(_ROBOT_LIMIT):
            for obsidian_robots in range(_ROBOT_LIMIT):
                for geode_robots in range(_ROBOT_LIMIT):
                    if geode_robots == 0:
                        continue
                    target_tuple = (ore_robots, clay_robots, obsidian_robots, geode_robots)
                    if target_tuple in search_table:
                        options = search_table[target_tuple]
                        for ts in options.keys():                            
                            for resources in options[ts]:
                                time_remaining = time_limit - ts + 1
                                minable_geodes = resources[_GEODE] + time_remaining*geode_robots
                                max_geodes = max(max_geodes, minable_geodes)
    return max_geodes

# Part 1
lines = get_input()
score = 0
time_limit = 24
for i in range(len(lines)):
    line = lines[i]
    robot_costs = parse_blueprint(line)
    print(robot_costs)
    search_table = build_geodes_table((robot_costs["ORE"],robot_costs["CLAY"],robot_costs["OBSIDIAN"],robot_costs["GEODE"]), time_limit)
    #pretty_print_build_options(search_table, (1,3,2,1))
    max_geodes = find_max_geodes(search_table, time_limit)
    
    print(max_geodes)
    print('')
    score += (i+1)*max_geodes
print('score', score)

# Part 2
lines = get_input()
scores = []
time_limit = 32
for i in range(0):
    line = lines[i]
    robot_costs = parse_blueprint(line)
    print('building search table')
    search_table = build_geodes_table((robot_costs["ORE"],robot_costs["CLAY"],robot_costs["OBSIDIAN"],robot_costs["GEODE"]), time_limit)
    #print("10", (2,4,0,0))
    #pretty_print_build_options(search_table, (2,4,0,0))
    #print("14", (2,7,1,0))
    #pretty_print_build_options(search_table, (2,7,1,0))
    #print("16", (2,7,2,0))
    #pretty_print_build_options(search_table, (2,7,2,0))
    #print("20", (2,7,4,0))
    #pretty_print_build_options(search_table, (2,7,4,0))
    #print("24", (2,7,5,3))
    #pretty_print_build_options(search_table, (2,7,5,3))
    
    print('looking through search table')
    max_geodes = find_max_geodes(search_table, time_limit)
    scores.append(max_geodes)
    print(time_limit, max_geodes)
    print('')
    break
product = 1
for score in scores:
    product *= score
print('scores', scores, product)

