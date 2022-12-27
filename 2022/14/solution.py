#!/usr/bin/env python3

import fileinput

def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

def find_grid_size(lines):
    max_x, min_x, max_y = None, None, None
    for line in lines:
        for coord in line.split(' -> '):
            x, y = coord.split(',')
            x, y = int(x), int(y)
            if max_x is None:
                max_x = x
            else:
                max_x = max(max_x, x)
            if max_y is None:
                max_y = y
            else:
                max_y = max(max_y, y)
            if min_x is None:
                min_x = x
            else:
                min_x = min(min_x, x)
    return max_x, min_x, max_y

def pretty_print(grid, min_x, max_x):
    return '\n'.join([''.join(row[min_x:max_x]) for row in grid])

def draw_rock_line(c1, c2, grid):
    def same_col(c1, c2):
        return c1[0] == c2[0]
    def same_row(c1, c2):
        return c1[1] == c2[1]
    if not same_col(c1, c2) and not same_row(c1, c2):
        raise Exception("Unexpected line draw", c1, c2)

    if same_col(c1, c2):
        col = c1[0]
        row_min = min(c1[1], c2[1])
        row_max = max(c1[1], c2[1])
        for row in range(row_min, row_max+1):
            grid[row][col] = '#'
    else:
        row = c1[1]
        col_min = min(c1[0], c2[0])
        col_max = max(c1[0], c2[0])
        for col in range(col_min, col_max+1):
            grid[row][col] = '#'
    return

def draw_rock_lines(line, grid):
    coords = line.split(' -> ')
    for i in range(len(coords)-1):
        c1 = coords[i].split(',')
        c2 = coords[i+1].split(',')
        c1 = (int(c1[0]), int(c1[1]))
        c2 = (int(c2[0]), int(c2[1]))
        
        draw_rock_line(c1, c2, grid)

def drop_sand(grid):
    grain_loc = (0, 500)
    max_depth = len(grid)
    while True:
        row, col = grain_loc
        if row+1 >= max_depth:
            # into the abyss
            return False
        
        if grid[row+1][col] == '.':
            grain_loc = (row+1, col)
        elif grid[row+1][col] in ['#', 'o']:
            if grid[row+1][col-1] == '.':
                # check down and to the left first
                grain_loc = (row+1, col-1)
            elif grid[row+1][col+1] == '.':
                # next check down and to the right
                grain_loc = (row+1, col+1)
            else:
                # comes to a rest
                grid[row][col] = 'o'
                return True
            
            
            
    
# Part 1
lines = get_input()
max_x, min_x, max_y = find_grid_size(lines)
grid = [['.']*(max_x+1) for i in range(max_y+1)]
for line in lines:
    draw_rock_lines(line, grid)

grains = 0
while drop_sand(grid):
    grains += 1

print(grains)

# Part 2
def drop_sand_part2(grid):
    grain_loc = (0, 500)
    floor = len(grid)

    if grid[0][500] == 'o':
        return False
    
    while True:
        row, col = grain_loc
        if row+2 >= floor:
            # floor hit
            grid[row][col] = 'o'
            return True
        
        if grid[row+1][col] == '.':
            grain_loc = (row+1, col)
        elif grid[row+1][col] in ['#', 'o']:
            if grid[row+1][col-1] == '.':
                # check down and to the left first
                grain_loc = (row+1, col-1)
            elif grid[row+1][col+1] == '.':
                # next check down and to the right
                grain_loc = (row+1, col+1)
            else:
                # comes to a rest
                grid[row][col] = 'o'
                return True

grid = [['.']*(2*max_x+1) for i in range(max_y+3)]
for line in lines:
    draw_rock_lines(line, grid)
grains = 0
while drop_sand_part2(grid):
    grains += 1
print("part 2:", grains)
    

