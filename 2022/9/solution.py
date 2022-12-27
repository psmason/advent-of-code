#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def move_down(c):
    return (c[0], c[1]-1)

def move_up(c):
    return (c[0], c[1]+1)

def move_left(c):
    return (c[0]-1, c[1])

def move_right(c):
    return (c[0]+1, c[1])

_HEAD_ACTIONS = {
    'U': move_up,
    'D': move_down,
    'L': move_left,
    'R': move_right,
}

_TAIL_ACTIONS = {
    'U': move_down,
    'D': move_up,
    'L': move_right,
    'R': move_left,
}

def is_connected(c1, c2):
    return (abs(c1[0]-c2[0]) <= 1) and (abs(c1[1]-c2[1]) <= 1)

# Part 1
lines = get_input()
_HEAD_COORD = (0,0)
_TAIL_COORD = (0,0)

_VISITED_COORDS = set()
for line in lines:
    direction, distance = line.split(' ')
    distance = int(distance)

    head_action = _HEAD_ACTIONS[direction]
    tail_action = _TAIL_ACTIONS[direction]
    for i in range(distance):
        _HEAD_COORD = head_action(_HEAD_COORD)
        if not is_connected(_HEAD_COORD, _TAIL_COORD):
            # reconnect relative to head position
            _TAIL_COORD = tail_action(_HEAD_COORD)
        _VISITED_COORDS.add(_TAIL_COORD)

print(len(_VISITED_COORDS))

# Part 2
def connect(head, tail):
    if tail[0] == head[0]:
        # same column
        y_move = (1 if tail[1] < head[1] else -1)
        return (tail[0], tail[1]+y_move)
    elif tail[1] == head[1]:
        # same row
        x_move = (1 if tail[0] < head[0] else -1)
        return (tail[0]+x_move, tail[1])
    else:
        # find the diagonal
        x_move = (1 if tail[0] < head[0] else -1)
        y_move = (1 if tail[1] < head[1] else -1)
        return (tail[0] + x_move, tail[1] + y_move)

_VISITED_COORDS.clear()
lines = get_input()
rope = [(0,0) for i in range(10)]
for line in lines:
    direction, distance = line.split(' ')
    distance = int(distance)

    head_action = _HEAD_ACTIONS[direction]
    for i in range(distance):
        rope[0] = head_action(rope[0])
        for k in range(1, len(rope)):
            if not is_connected(rope[k-1], rope[k]):
                rope[k] = connect(rope[k-1], rope[k])
        _VISITED_COORDS.add(rope[-1])
print(len(_VISITED_COORDS))
