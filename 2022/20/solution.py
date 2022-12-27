#!/usr/bin/env python3

import fileinput
from collections import defaultdict

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def get_numbers_from_node(node):
    result = []
    start = node["VALUE"]
    current = node
    while True:
        result.append(current["VALUE"])
        current = current["NEXT"]
        if current["VALUE"] == start:
            return result

def get_numbers_from_node_reversed(node):
    result = []
    start = node["VALUE"]
    current = node
    while True:
        result.append(current["VALUE"])
        current = current["PREVIOUS"]
        if current["VALUE"] == start:
            return result

def build_linked_list(encrypted):
    current_node = {
        "VALUE"    : encrypted[0],
        "NEXT"     : {},
        "PREVIOUS" : {},
        "INDEX"    : 0,
    }
    beg_node = current_node
    zero_node, end_node = None, None

    i = 0
    previous_node = None
    while True:
        if i == len(encrypted):
            break

        current_node["VALUE"] = encrypted[i]
        current_node["INDEX"] = i
        end_node = current_node

        current_node["NEXT"] = {}
        current_node["NEXT"]["PREVIOUS"] = current_node
        if previous_node != None:
            current_node["PREVIOUS"] = previous_node
        else:
            current_node["PREVIOUS"] = {}
        current_node["PREVIOUS"]["NEXT"] = current_node

        if encrypted[i] == 0:
            zero_node = current_node
        previous_node = current_node
        current_node = current_node["NEXT"]
        i += 1
    # Making the list circular
    beg_node["PREVIOUS"] = end_node
    end_node["NEXT"] = beg_node
    
    return zero_node

def init_position_table(zero_node):
    position_table = {}
    current = zero_node
    while True:
        position_table[current["INDEX"]] = current
        current = current["NEXT"]
        if current["VALUE"] == 0:
            return position_table

def start_mixing(encrypted, position_table):
    print('starting to mix')

    for i in range(len(encrypted)):
        number_to_mix = encrypted[i]
        if number_to_mix == 0:
            # Nothing to do
            continue

        node_to_mix   = position_table[i]
        previous_node = node_to_mix["PREVIOUS"]
        next_node     = node_to_mix["NEXT"]

        position_table[previous_node["INDEX"]]["NEXT"] = next_node
        position_table[next_node["INDEX"]]["PREVIOUS"] = previous_node

        shifts_required = number_to_mix
        new_node = None
        if shifts_required > 0:
            new_node = next_node
            shifts_required = shifts_required % (len(encrypted)-1)
            for _ in range(shifts_required):
                new_node = new_node["NEXT"]
        else:
            new_node = previous_node
            shifts_required = abs(shifts_required) % (len(encrypted)-1)
            for _ in range(shifts_required-1):
                new_node = new_node["PREVIOUS"]

        new_previous_node = new_node["PREVIOUS"]

        position_table[new_previous_node["INDEX"]]["NEXT"] = node_to_mix
        position_table[new_node["INDEX"]]["PREVIOUS"] = node_to_mix

        position_table[i]["PREVIOUS"] = position_table[new_previous_node["INDEX"]]
        position_table[i]["NEXT"]     = position_table[new_node["INDEX"]]
    
# Part 1
encrypted = [int(line.strip()) for line in get_input()]
zero_node = build_linked_list(encrypted)
position_table = init_position_table(zero_node)
start_mixing(encrypted, position_table)
    
print('getting numbers from zero')
numbers_from_zero = get_numbers_from_node(zero_node)
print(numbers_from_zero[1000 % len(numbers_from_zero)])
answer = numbers_from_zero[1000 % len(numbers_from_zero)]
print(numbers_from_zero[2000 % len(numbers_from_zero)])
answer += numbers_from_zero[2000 % len(numbers_from_zero)]
print(numbers_from_zero[3000 % len(numbers_from_zero)])
answer += numbers_from_zero[3000 % len(numbers_from_zero)]
print(answer)

# Part 2
encrypted = [811589153*int(line.strip()) for line in get_input()]
zero_node = build_linked_list(encrypted)
position_table = init_position_table(zero_node)

for i in range(10):
    start_mixing(encrypted, position_table)
    
numbers_from_zero = get_numbers_from_node(zero_node)
print(numbers_from_zero[1000 % len(numbers_from_zero)])
answer = numbers_from_zero[1000 % len(numbers_from_zero)]
print(numbers_from_zero[2000 % len(numbers_from_zero)])
answer += numbers_from_zero[2000 % len(numbers_from_zero)]
print(numbers_from_zero[3000 % len(numbers_from_zero)])
answer += numbers_from_zero[3000 % len(numbers_from_zero)]
print(answer)
    
