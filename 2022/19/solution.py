#!/usr/bin/env python3

import copy
import fileinput
import math
import re
from collections import defaultdict

_ROBOT_LIMIT = 20
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

def find_max_geodes_dfs(robot_costs, time_limit):
    """
    With DFS, the idea is that we can quickly probe for potential solutions, 
    and then efficiently prune other branches based on the best solution found 
    so far.
    """

    def make_build_options(current_robots, max_robots_tuple):
        result = []

        # Greedily try to build in this order: geode, obsidian, clay, ore.
        # This speeds up finding potential solutions yielding geode.
        for i in range(len(current_robots)):
            option = list(current_robots)
            
            if i in [0,1,2] and option[i] > max_robots_tuple[i]:
                # Skip builds we know don't help.
                continue

            if i == 2 and option[1] == 0:
                # can't build obsidian without clay robots
                continue

            if i == 3 and option[2] == 0:
                # can't build geode without obsidian robots
                continue
            
            option[i] += 1
            result.append((tuple(option), i))
        return result

    def compute_time_to_build(starting_resources, available_robots, robot_cost):
        max_time_needed_for_resources = -1
        for i in range(len(robot_cost)):
            if robot_cost[i] == 0:
                continue
            time_needed_for_resource = math.ceil(max(0, robot_cost[i]-starting_resources[i]) / available_robots[i])
            max_time_needed_for_resources = max(max_time_needed_for_resources, time_needed_for_resource)
        # Plus time to build
        return max_time_needed_for_resources + 1

    def compute_new_resource_tuple(starting_resources, available_robots, time_delta, robot_cost):
        result = list(starting_resources)
        for r in [_ORE, _CLAY, _OBSIDIAN, _GEODE]:
            result[r] += available_robots[r]*time_delta
        # Deducting however much the robot cost.
        for r in [_ORE, _CLAY, _OBSIDIAN]:
            result[r] -= robot_cost[r]
        return tuple(result)

    def should_prune_branch(best_solution_so_far, current_robots, current_resources, current_time, time_limit):
        time_remaining = time_limit - current_time

        # Assume that for each remaining minute, we build a geode robot, even if that isn't possible.
        potential_geodes = current_resources[_GEODE]
        geode_robots = current_robots[_GEODE]
        for i in range(time_remaining+1):
            potential_geodes += geode_robots
            geode_robots += 1
        if potential_geodes < best_solution_so_far:
            return True
        
        return False
        
    # So that we don't build unnecessary robots
    max_robots_tuple = [-1, -1, -1]
    for costs in list(robot_costs):
        max_robots_tuple[0] = max(max_robots_tuple[0], costs[0])
        max_robots_tuple[1] = max(max_robots_tuple[1], costs[1])
        max_robots_tuple[2] = max(max_robots_tuple[2], costs[2])
    max_robots_tuple = tuple(max_robots_tuple)

    max_geodes = 0
    current_time = 1
    visit_queue = []
    # Starting with just one ore robot.
    visit_queue.append(((1, 0, 0, 0), (0,0,0,0), current_time))

    while len(visit_queue) > 0:
        current_robots, current_resources, current_time = visit_queue.pop()

        if should_prune_branch(max_geodes, current_robots, current_resources, current_time, time_limit):
            continue
        
        build_options = make_build_options(current_robots, max_robots_tuple)
        for option in build_options:
            target_robots, robot_to_build = option
            robot_to_build_cost = robot_costs[robot_to_build]
            
            time_needed = compute_time_to_build(current_resources, current_robots, robot_to_build_cost)
            if current_time + time_needed > time_limit:
                # This branch has exhausted available time. Time to compute how many geodes
                # we can get. 
                branch_time_remaining = time_limit - current_time + 1
                minable_geodes = current_resources[_GEODE] + branch_time_remaining*current_robots[_GEODE]
                max_geodes = max(max_geodes, minable_geodes)
            else:
                new_resources = compute_new_resource_tuple(current_resources, current_robots, time_needed, robot_to_build_cost)
                visit_queue.append((target_robots, new_resources, current_time+time_needed))                        
        
    return max_geodes
        
# Part 1
lines = get_input()
score = 0
time_limit = 24
for i in range(len(lines)):
    line = lines[i]
    robot_costs = parse_blueprint(line)
    max_geodes = find_max_geodes_dfs((robot_costs["ORE"],robot_costs["CLAY"],robot_costs["OBSIDIAN"],robot_costs["GEODE"]), time_limit)
    score += (i+1)*max_geodes
print('part 1 score', score)

# Part 2
lines = get_input()
scores = []
time_limit = 32
# Only the first three blueprints
for i in range(min(3, len(lines))):
    line = lines[i]
    robot_costs = parse_blueprint(line)
    max_geodes = find_max_geodes_dfs((robot_costs["ORE"],robot_costs["CLAY"],robot_costs["OBSIDIAN"],robot_costs["GEODE"]), time_limit)
    scores.append(max_geodes)
    
product = 1
for score in scores:
    product *= score
print('part 2 scores', scores, product)
