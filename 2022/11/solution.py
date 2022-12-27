#!/usr/bin/env python3

import fileinput
from functools import reduce


def get_input():
    lines = []
    with fileinput.input(files=('input.txt')) as f:
        for line in f:
            lines.append(line.strip())
        return lines

class Monkey:
    def __init__(self, starting_items, operation, test):
        self.items = starting_items
        self.operation = operation
        self.test = test
        self.items_inspected = 0
        
# example
#monkeys = [
#    Monkey([79, 98], lambda x: x*19, lambda x: 2 if x%23 == 0 else 3),
#    Monkey([54, 65, 75, 74], lambda x: x+6, lambda x: 2 if x%19 == 0 else 0),
#    Monkey([79, 60, 97], lambda x: x*x, lambda x: 1 if x%13 == 0 else 3),
#    Monkey([74], lambda x: x+3, lambda x: 0 if x%17 == 0 else 1),
#]

# input
monkeys = [
    Monkey([54, 61, 97, 63, 74],             lambda x: x*7,  lambda x: 5 if x%17 == 0 else 3),
    Monkey([61, 70, 97, 64, 99, 83, 52, 87], lambda x: x+8,  lambda x: 7 if x%2 == 0 else 6),
    Monkey([60, 67, 80, 65],                 lambda x: x*13, lambda x: 1 if x%5 == 0 else 6),
    Monkey([61, 70, 76, 69, 82, 56],         lambda x: x+7,  lambda x: 5 if x%3 == 0 else 2),
    Monkey([79, 98],                         lambda x: x+2,  lambda x: 0 if x%7 == 0 else 3),
    Monkey([72, 79, 55],                     lambda x: x+1,  lambda x: 2 if x%13 == 0 else 1),
    Monkey([63],                             lambda x: x+4,  lambda x: 7 if x%19 == 0 else 4),
    Monkey([72, 51, 93, 63, 80, 86, 81],     lambda x: x*x,  lambda x: 0 if x%11 == 0 else 4),
]

for round in range(20):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            monkey.items_inspected += 1
            
            item = monkey.items.pop()
            item = monkey.operation(item)
            item = item // 3
            
            target = monkey.test(item)
            monkeys[target].items.append(item)
print(sorted([m.items_inspected for m in monkeys]))

# Part 2

#monkeys = [
#    Monkey([79, 98],         lambda x: x*19, lambda x: 2 if x%23 == 0 else 3),
#    Monkey([54, 65, 75, 74], lambda x: x+6,  lambda x: 2 if x%19 == 0 else 0),
#    Monkey([79, 60, 97],     lambda x: x*x,  lambda x: 1 if x%13 == 0 else 3),
#    Monkey([74],             lambda x: x+3,  lambda x: 0 if x%17 == 0 else 1),
#]

monkeys = [
    Monkey([54, 61, 97, 63, 74],             lambda x: x*7,  lambda x: 5 if x%17 == 0 else 3),
    Monkey([61, 70, 97, 64, 99, 83, 52, 87], lambda x: x+8,  lambda x: 7 if x%2 == 0 else 6),
    Monkey([60, 67, 80, 65],                 lambda x: x*13, lambda x: 1 if x%5 == 0 else 6),
    Monkey([61, 70, 76, 69, 82, 56],         lambda x: x+7,  lambda x: 5 if x%3 == 0 else 2),
    Monkey([79, 98],                         lambda x: x+2,  lambda x: 0 if x%7 == 0 else 3),
    Monkey([72, 79, 55],                     lambda x: x+1,  lambda x: 2 if x%13 == 0 else 1),
    Monkey([63],                             lambda x: x+4,  lambda x: 7 if x%19 == 0 else 4),
    Monkey([72, 51, 93, 63, 80, 86, 81],     lambda x: x*x,  lambda x: 0 if x%11 == 0 else 4),
]

for round in range(10*1000):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            monkey.items_inspected += 1
            
            item = monkey.items.pop()
            item = monkey.operation(item)

            # bound by the divisors: 13*17*19*23 in the example
            # bound by the divisors: 2*3*5*7*11*13*17*19 in the input
            #
            # This works because x mod n == (x mod (k*n)) mod n, and
            # to find a multiple working for all divisors, use the 
            # product of all divisors.
            new_item_value = item % 9699690
                
            target = monkey.test(item)
            monkeys[target].items.append(new_item_value)
            
print(sorted([m.items_inspected for m in monkeys]))
