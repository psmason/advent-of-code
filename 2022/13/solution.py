#!/usr/bin/env python3

import fileinput
import re
from functools import cmp_to_key

_BRACKET_RE = re.compile("^\[(.*)\]$")

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def split_top_level(s):
    if not s:
        return []
    
    bracket_count = 0
    splits = []
    for i in range(len(s)):
        c = s[i]
        if c == '[':
            bracket_count += 1
        elif c == ']':
            bracket_count -= 1
        elif c == ',' and bracket_count == 0:
            splits.append(i)            

    if len(splits) == 0:
        return [s]

    result = []
    start = 0
    for split in splits:
        result.append(s[start:split])
        start = split+1
    last_split = splits[-1]+1
    result.append(s[last_split:])
    return result

def compare(lhs, rhs):
    lhs_bracket_match = _BRACKET_RE.match(lhs)
    rhs_bracket_match = _BRACKET_RE.match(rhs)
    if not lhs_bracket_match and not rhs_bracket_match:
        # Nothing else to recurse
        if lhs == rhs:
            return 0
        if int(lhs) < int(rhs):
            return -1
        return 1

    if not lhs_bracket_match:
        lhs = '[' + lhs + ']'
    if not rhs_bracket_match:
        rhs = '[' + rhs + ']'
    lhs_packets = _BRACKET_RE.findall(lhs)
    rhs_packets = _BRACKET_RE.findall(rhs)
    if len(lhs_packets) > 1:
        raise Exception("Unexpected lhs parse: ", lhs, lhs_packets)
    if len(rhs_packets) > 1:
        raise Exception("Unexpected rhs parse: ", rhs, rhs_packets)

    lhs_packets = split_top_level(lhs_packets[0])
    rhs_packets = split_top_level(rhs_packets[0])
    for i in range(min(len(lhs_packets), len(rhs_packets))):
        lhs_packet = lhs_packets[i]
        rhs_packet = rhs_packets[i]

        # The recursive call
        compare_result = compare(lhs_packet, rhs_packet)
        if compare_result not in [0, None]:
            return compare_result

    if len(lhs_packets) == len(rhs_packets):
        return 0
    elif len(rhs_packets) < len(lhs_packets):
        # If the right list runs out of items first, the inputs are not in the right order
        return 1
    else:
        return -1


# Part 1
lines = get_input()
results = []
for i in range(0, len(lines), 3):
    lhs, rhs = lines[i], lines[i+1]
    if compare(lhs, rhs) == compare(rhs, lhs):
        print(lhs)
        print(rhs)
        print(compare(lhs, rhs), compare(rhs, lhs))
        raise Exception('inconsistency', lhs, rhs)
    compare_result = compare(lhs, rhs)
    results.append((compare_result, i // 3 + 1))

print(results)
print(sum([r[1] for r in results if r[0] < 0]))
print('number of zero results', sum([r[1] for r in results if r[0] == 0]))
    
# Part 2
all_lines = [line for line in lines if len(line)>0]
all_lines.append('[[2]]')
all_lines.append('[[6]]')

sorted_lines = sorted(all_lines, key=cmp_to_key(compare))
print((sorted_lines.index('[[2]]')+1)*(sorted_lines.index('[[6]]')+1))
