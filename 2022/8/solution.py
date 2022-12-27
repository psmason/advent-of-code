#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def build_grid(lines):
    rows = len(lines)
    cols = len(lines[0])
    grid = [[None]*cols for i in range(rows)]
    
    for row in range(rows):
        line = lines[row]
        for col in range(cols):
            grid[row][col] = (row, col, int(line[col]))
    return grid

def get_row(grid, row):
    return grid[row]

def get_column(grid, col):
    return [r[col] for r in grid]

lines = get_input()
grid = build_grid(lines)

_VISIBLE_TREES = set()

def find_visible_trees(trees):
    tree_line = -1
    
    for tree in trees:
        tree_row, tree_col, tree_height = tree
        if tree_line < tree_height:
            _VISIBLE_TREES.add((tree_row, tree_col))
            tree_line = tree_height

for row in range(len(grid)):
    # from the left
    find_visible_trees(get_row(grid, row))

    # from the right
    find_visible_trees(get_row(grid, row)[::-1])


for col in range(len(grid[0])):
    # from the top
    find_visible_trees(get_column(grid, col))

    # from the bottom
    find_visible_trees(get_column(grid, col)[::-1])

# Part 1
print(len(_VISIBLE_TREES))

# Part 2
def calc_tree_score(grid, tree):
    tree_row, tree_col, tree_height = tree
    rows = len(grid)
    cols = len(grid[0])
    
    def visible_to_the_right(grid):
        count = 0
        for col in range(tree_col+1, cols):
            count += 1
            if tree_height <= grid[tree_row][col][2]:
                break
        return count

    def visible_to_the_left(grid):
        count = 0
        for col in range(tree_col-1, -1, -1):
            count += 1
            if tree_height <= grid[tree_row][col][2]:
                break
        return count

    def visible_below(grid):
        count = 0
        for row in range(tree_row+1, rows):
            count += 1
            if tree_height <= grid[row][tree_col][2]:
                break
        return count

    def visible_above(grid):
        count = 0
        for row in range(tree_row-1, -1, -1):
            count += 1
            if tree_height <= grid[row][tree_col][2]:
                break
        return count

    return visible_to_the_right(grid) * visible_to_the_left(grid) * visible_below(grid) * visible_above(grid)

max_tree_score = -1
for row in range(len(grid)):
    for col in range(len(grid[0])):
        max_tree_score = max(max_tree_score, calc_tree_score(grid, grid[row][col]))
print(max_tree_score)

#print(grid)
#print(get_row(grid, 4))
#print(get_column(grid, 2))
