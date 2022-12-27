#!/usr/bin/env python3

import fileinput
import re

from collections import defaultdict

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line)
        return lines

_STACKS = defaultdict(list)

def pretty_print_stack():
    for i in sorted(_STACKS.keys()):
        print(i, _STACKS[i])
    
def parse_stacks(lines):
    label_matcher = re.compile("[A-Z]")
    for i in range(len(lines)):
        line = lines[i]
        matches = list(label_matcher.finditer(line))
        if matches:
            for m in matches:
                stack = int(m.start()/4) + 1
                _STACKS[stack].insert(0,m.group())
        else:
            return lines[i+2:]

def make_moves(lines):
    move_matcher = re.compile("move ([0-9]+?) from ([0-9]+?) to ([0-9]+?)")
    for line in lines:
        result = move_matcher.findall(line)
        if result:
            parsed_amt, parsed_from, parsed_to = [int(c) for c in result[0]]
            for i in range(parsed_amt):
                _STACKS[parsed_to].append(_STACKS[parsed_from].pop())
        else:
            return

def make_moves_9001(lines):
    move_matcher = re.compile("move ([0-9]+?) from ([0-9]+?) to ([0-9]+?)")
    for line in lines:
        result = move_matcher.findall(line)
        if result:
            parsed_amt, parsed_from, parsed_to = [int(c) for c in result[0]]
            _STACKS[parsed_to] += _STACKS[parsed_from][-parsed_amt:]
            _STACKS[parsed_from] = _STACKS[parsed_from][:-parsed_amt]
        else:
            return


remaining_lines = parse_stacks(get_input())
make_moves(remaining_lines)
print(''.join([_STACKS[i][-1] for i in sorted(_STACKS.keys())]))

_STACKS.clear()
remaining_lines = parse_stacks(get_input())
make_moves_9001(remaining_lines)
print(''.join([_STACKS[i][-1] for i in sorted(_STACKS.keys())]))
