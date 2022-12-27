#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def find_first_marker(line, marker_size):
    if len(line) < marker_size:
        raise Exception("unexpected line length: " + line)
    for i in range(marker_size, len(line)):
        if len(set(line[i-marker_size:i])) == marker_size:
            return i
    raise Exception("found no marker for line: " + line)
    
# part 1
lines = ['bvwbjplbgvbhsrlpgdmjqwftvncz',
         'nppdvjthqldpwncqszvftbrmjlhg',
         'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
         'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']

# part 2
lines = ['mjqjpqmgbljsphdztnvjfqwrcgsmlb',
         'bvwbjplbgvbhsrlpgdmjqwftvncz',
         'nppdvjthqldpwncqszvftbrmjlhg',
         'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
         'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']

lines = get_input()
sum = 0
for line in lines:
    print(find_first_marker(line, 14), line)
    sum += find_first_marker(line, 14)
print(sum)

