#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def check_if_fully_contained(line):
    def contains(i1, i2):
        # does interval1 contain iterval2?
        return (i1[0] <= i2[0]) and (i1[1] >= i2[1])
    lhs, rhs = line.split(',')
    lhs, rhs = lhs.split('-'), rhs.split('-')
    lhs, rhs = [int(s) for s in lhs], [int(s) for s in rhs]
    return contains(lhs, rhs) or contains(rhs, lhs)

def check_if_overlapped(line):
    def overlaps(i1, i2):
        if i1[1] < i2[0]:
            return False
        return i1[0] <= i2[1]
        
    lhs, rhs = line.split(',')
    lhs, rhs = lhs.split('-'), rhs.split('-')
    lhs, rhs = [int(s) for s in lhs], [int(s) for s in rhs]  
    return overlaps(lhs, rhs)

lines = get_input()
count = 0
for line in lines:
    if check_if_fully_contained(line):
        count += 1
print(count)


lines = get_input()
count = 0
for line in lines:
    if check_if_overlapped(line):
        count += 1
print(count)
