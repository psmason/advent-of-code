#!/usr/bin/env python3

import fileinput
from collections import defaultdict

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

lines = get_input()
food = defaultdict(list)

elf = 0
for line in lines:
    if line:
      food[elf].append(int(line))
    else:
        elf += 1

# Part 1: how many calories are being carried by the elf with the most calories?
print(max([sum(pack) for pack in food.values()]))

# Part 2: Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
print(sum(sorted([sum(pack) for pack in food.values()], reverse=True)[0:3]))
    
