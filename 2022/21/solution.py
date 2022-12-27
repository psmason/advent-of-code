#!/usr/bin/env python3

import copy
import fileinput
import re

from collections import deque

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

_NAME           = "name"
_NUMBER         = "number"
_INCOMING_EDGES = "incoming_edges"
_OUTGOING_EDGES = "outgoing_edges"
_OPERATOR       = "operator"
_LHS            = "lhs"
_RHS            = "rhs"

def topological_sort(lines):
    def get_or_create_node(node_table, monkey):
        if monkey in node_table:
            return node_table[monkey]
        return {
            _NAME: monkey,
            _INCOMING_EDGES: set(),
            _OUTGOING_EDGES: set(),
        }  
    
    yells_number = re.compile('^([a-z]+): ([-]?[0-9]+)$')
    waits        = re.compile('^([a-z]+): ([a-z]+) ([+-/*]) ([a-z]+)$')

    # Kahn's algorithms
    node_table = {}
    traversal = deque()
    
    for line in lines:
        if yells_number.match(line):
            monkey, number = yells_number.findall(line)[0]
            node = get_or_create_node(node_table, monkey)
            node[_NUMBER] = int(number)
            node_table[monkey] = node
            traversal.append(node)
        elif waits.match(line):
            monkey, lhs, operator, rhs = waits.findall(line)[0]

            lhs_node = get_or_create_node(node_table, lhs)
            lhs_node[_OUTGOING_EDGES].add(monkey)
            node_table[lhs] = lhs_node
            
            rhs_node = get_or_create_node(node_table, rhs)
            rhs_node[_OUTGOING_EDGES].add(monkey)
            node_table[rhs] = rhs_node
            
            node = get_or_create_node(node_table, monkey)
            node[_OPERATOR] = operator
            node[_LHS] = lhs
            node[_RHS] = rhs
            node[_INCOMING_EDGES].add(lhs)
            node[_INCOMING_EDGES].add(rhs)
            node_table[monkey] = node

    sorted_monkeys = []
    while len(traversal) > 0:
        current_monkey = traversal.popleft()
        name = current_monkey[_NAME]
        sorted_monkeys.append(name)
        for dependent_monkey in node_table[name][_OUTGOING_EDGES]:
            node_table[dependent_monkey][_INCOMING_EDGES].remove(name)
            if len(node_table[dependent_monkey][_INCOMING_EDGES]) == 0:
                traversal.append(node_table[dependent_monkey])
                    
    return node_table, sorted_monkeys

def run_calculation(node_table, sorted_monkeys):
    for monkey in sorted_monkeys:
        node = node_table[monkey]
        if _OPERATOR not in node:
            # Nothing to do
            continue

        lhs_node = node_table[node[_LHS]]
        rhs_node = node_table[node[_RHS]]        
        if _NUMBER not in lhs_node:
            raise Exception(lhs_node[_NAME], "is missing the required number")
        if _NUMBER not in rhs_node:
            raise Exception(rhs_node[_NAME], "is missing the required number")

        lhs_arg, rhs_arg = lhs_node[_NUMBER], rhs_node[_NUMBER]
        if node[_OPERATOR] == "*":
            node[_NUMBER] = lhs_arg * rhs_arg
        elif node[_OPERATOR] == "/":
            node[_NUMBER] = lhs_arg / rhs_arg
        elif node[_OPERATOR] == "+":
            node[_NUMBER] = lhs_arg + rhs_arg
        elif node[_OPERATOR] == "-":
            node[_NUMBER] = lhs_arg - rhs_arg
        elif node[_OPERATOR] == "==":
            #print('root check', lhs_arg, rhs_arg)
            return int(lhs_arg) == int(rhs_arg)
        node_table[monkey] = node

def run_calculation_humn(node_table, sorted_monkeys):
    def make_callable(lhs, rhs, operator):
        if node[_OPERATOR] == "*":
            if callable(lhs) and callable(rhs):
                return lambda x: lhs(x) * rhs(x)
            elif callable(lhs_arg):
                return lambda x: lhs(x) * rhs
            elif callable(rhs_arg):
                return lambda x: lhs * rhs(x)
        elif node[_OPERATOR] == "/":
            if callable(lhs) and callable(rhs):
                return lambda x: lhs(x) / rhs(x)
            elif callable(lhs_arg):
                return lambda x: lhs(x) / rhs
            elif callable(rhs_arg):
                return lambda x: lhs / rhs(x)
        elif node[_OPERATOR] == "+":
            if callable(lhs) and callable(rhs):
                return lambda x: lhs(x) + rhs(x)
            elif callable(lhs_arg):
                return lambda x: lhs(x) + rhs
            elif callable(rhs_arg):
                return lambda x: lhs + rhs(x)
        elif node[_OPERATOR] == "-":
            if callable(lhs) and callable(rhs):
                return lambda x: lhs(x) - rhs(x)
            elif callable(lhs_arg):
                return lambda x: lhs(x) - rhs
            elif callable(rhs_arg):
                return lambda x: lhs - rhs(x)

    def calc_const(lhs, rhs, operator):
        if node[_OPERATOR] == "*":
            return lhs * rhs
        elif node[_OPERATOR] == "/":
            return lhs / rhs
        elif node[_OPERATOR] == "+":
            return lhs + rhs
        elif node[_OPERATOR] == "-":
            return lhs - rhs
        
    for monkey in sorted_monkeys:
        node = node_table[monkey]
        if _OPERATOR not in node:
            # Nothing to do
            continue

        lhs_node = node_table[node[_LHS]]
        rhs_node = node_table[node[_RHS]]        
        if _NUMBER not in lhs_node:
            raise Exception(lhs_node[_NAME], "is missing the required number")
        if _NUMBER not in rhs_node:
            raise Exception(rhs_node[_NAME], "is missing the required number")

        lhs_arg, rhs_arg = lhs_node[_NUMBER], rhs_node[_NUMBER]
        if not callable(lhs_arg) and not callable(rhs_arg):
            node[_NUMBER] = calc_const(lhs_arg, rhs_arg, node[_OPERATOR])
        elif node[_OPERATOR] == "==":
            #print('root check', lhs_arg, rhs_arg)
            return lhs_arg, rhs_arg
        else:
            node[_NUMBER] = make_callable(lhs_arg, rhs_arg, node[_OPERATOR])
        node_table[monkey] = node

# Part 1
print('running topological sort')
node_table, sorted_monkeys = topological_sort(get_input())
print('running calculation')
run_calculation(node_table, sorted_monkeys)
print(node_table["root"][_NUMBER])

# Part 2
node_table, sorted_monkeys = topological_sort(get_input())
node_table['root'][_OPERATOR] = '=='
node_table['humn'][_NUMBER] = lambda x: x
lhs, rhs = run_calculation_humn(node_table, sorted_monkeys)

# The lhs function is hopefully strictly decreasing as x increases.
# So we can do a binary search.
x = 1
lower_bound, upper_bound = x, None
while True:
    if lhs(x) < rhs:
        upper_bound = x
        break
    else:
        lower_bound = x
    x *= 2
print("bounds", lower_bound, upper_bound)

answer = None
while True:
    mid = (lower_bound + upper_bound) / 2
    mid = int(mid)

    attempt = lhs(mid)
    if attempt < rhs:
        upper_bound = mid
    elif attempt > rhs:
        lower_bound = mid
    else:
        answer = mid
        break
print(answer, lhs(answer), rhs)
