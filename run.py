#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import random

rand_generator = random.SystemRandom()
alphabet= (u"abcdefghijklmnopqrstuvwxyz"
          u"èéêëēėęÿûüùúūîïíīįìôöòóœøōõàáâäæãåāßśšłžźżçćčñń")

def random_char(alph):
    char = alph[rand_generator.randrange(len(alph))]
    return char


def random_num(alph):
    return rand_generator.randrange(len(alph))


def generate_line(alphabet):
    array = [ch for ch in alphabet]
    line = []
    for i in range(len(alphabet)):
        line.append(array.pop(random_num(array)))

    return line


def mix_rows(grid):
    index1 = rand_generator.randrange(len(grid))
    index2 = rand_generator.randrange(len(grid))
    while (index1 == index2):
        index2 = rand_generator.randrange(len(grid))

    grid[index1],grid[index2] = grid[index2],grid[index1]


def mix_cols(grid):
    index1 = rand_generator.randrange(len(grid))
    index2 = rand_generator.randrange(len(grid))
    while (index1 == index2):
        index2 = rand_generator.randrange(len(grid))

    for row in grid:
        row[index1],row[index2] = row[index2],row[index1]

def mix_grid(grid):
    iterations = rand_generator.randrange(100*len(grid),1000*len(grid))
    i = 0
    while i < iterations:
        row_or_column = rand_generator.randrange(1)

        if row_or_column == 1:
            mix_cols(grid)
        else:
            mix_rows(grid)

        i += 1


def generate_grid(alphabet):
    random_line = generate_line(alphabet)
    array = random_line[:]
    grid = []
    for i in range(len(random_line)):
        new_Array = array[:]
        grid.append(new_Array)
        last_char = array.pop()
        array.insert(0, last_char)

    mix_grid(grid)

    return grid


def check_norepeat(grid):
    def conflict(grid, row, col):
        char = grid[row][col]
        r = grid[row]
        c = [row[col] for row in grid]

        rowcount = r.count(char)
        colcount = c.count(char)

        if (rowcount!=1) or (colcount!=1):
            return True

        return False

    norepeat = True

    for row in range(len(grid)):
        for col in range(len(grid)):
            if (conflict(grid, row, col)):
                norepeat = False

    return norepeat

grid = generate_grid(alphabet)

for row in grid:
    print (''.join(row))


def test():
    grid_array = []
    conflict_list = []
    for i in range(100):
        grid = generate_grid(alphabet)

        grid_array.append(grid)
        norepeat = check_norepeat(grid)

        if norepeat:
            print ("Test case "), (i),(":OK")
        else:
            print ("Test case "), (i), (":FAILED")
            conflict_list.append(i)

    print (conflict_list)

grid = generate_grid(alphabet)

for row in grid:
    print (''.join(row))


#test()
