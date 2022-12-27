#!/usr/bin/env python3

import fileinput
import re

from collections import defaultdict

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

_TRAVERSED_FILES = set()
_TRAVERSAL_STACK = []
_DIRECTORY_SIZES = defaultdict(int)

def directory_path():
    return '/'.join(_TRAVERSAL_STACK)

def run_commands(lines):
    cd_dir_matcher = re.compile("\$ cd ([a-z]+?)$")
    file_size_matcher = re.compile("([0-9]+?) ([a-z.]+?)$")

    for line in lines:
        if line[0:4] == '$ cd':
            if line[-1] == '/':
                _TRAVERSAL_STACK.clear()
            elif line[-2:] == '..':
                _TRAVERSAL_STACK.pop()
            else:
                next_dir = cd_dir_matcher.findall(line)
                if not next_dir:
                    raise Exception('Failed to parse directory: ' + line)
                if len(next_dir) != 1:
                    raise Exception('Unexpected parse match: ' + line + ' :: ' + ','.join(next_dir))
                _TRAVERSAL_STACK.append(next_dir[0])
        elif file_size_matcher.match(line):
            for match in file_size_matcher.findall(line):
                file_size, file_name = match
                file_size = int(file_size)
                full_file_name = directory_path() + '/' + file_name
                if full_file_name not in _TRAVERSED_FILES:
                    _TRAVERSED_FILES.add(full_file_name)
                    for i in range(len(_TRAVERSAL_STACK)+1):
                        d = '/' + '/'.join(_TRAVERSAL_STACK[:i])
                        _DIRECTORY_SIZES[d] += file_size

lines = get_input()
run_commands(lines)

sum = 0
for k,v in _DIRECTORY_SIZES.items():
    #print(k,v)
    if v <= 100*1000:
        sum += v
print(sum)

# Sorting by directory sizes
unused_space = 70*1000*1000 - _DIRECTORY_SIZES['/']
sorted_directories = sorted(_DIRECTORY_SIZES.items(), key=lambda x: x[1])
for d in sorted_directories:
    if unused_space + d[1] >= 30*1000*1000:
        print(d)
        break
