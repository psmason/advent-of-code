#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def get_priority(c):
    if c.islower():
        return ord(c)-ord('a')+1
    else:
        return ord(c)-ord('A')+27

def check_rucksack(line):
    split = int(len(line)/2)
    c1, c2 = line[0:split], line[split:]
    c1, c2 = set([c for c in c1]), set([c for c in c2])

    if len(c1.intersection(c2)) != 1:
        raise Exception("Unexpected intersection result for line " + line)
    misplaced_item = list(c1.intersection(c2))[0]
    return get_priority(misplaced_item)

lines = get_input()
print(sum([check_rucksack(l) for l in lines]))

def find_badge(lines):
    c1 = set([c for c in lines[0]])
    c2 = set([c for c in lines[1]])
    c3 = set([c for c in lines[2]])

    badge = list(c1.intersection(c2).intersection(c3))
    if len(badge)>1:
        raise Exception("Unexpected bdage intersection result")

    return get_priority(badge[0])


i = 0
sum = 0
lines = get_input()
while i < len(lines):
    sum += find_badge(lines[i:i+3])
    i += 3
print(sum)
    
