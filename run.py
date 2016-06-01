#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, getopt
import codecs
import random

rand_generator = random.SystemRandom()
default_alphabet= (u"abcdefghijklmnopqrstuvwxyz"
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


def save_to_file(grid, filepath):
    outfile = codecs.open(filepath, mode='w+', encoding='utf-8')
    outfile.writelines([ ((''.join(row)) + u'\n') for row in grid ])

def alphabet_from_file(filepath):
    alph = codecs.open(filepath, encoding='utf-8').readline()
    # Remove newline
    alph = alph[:-1]
    return alph


def test(alphabet):
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


def main(argv):
    inname = ''
    alphabet = default_alphabet
    outname=''

    try:
        opts, args = getopt.getopt(argv, "i:o:a:")
    except getopt.GetoptError:
        # TODO: Print help for the user
        sys.exit(2)

    # Processing options
    for option, argument in opts:
        if option=="-i":
            if argument is not None:
                inname = argument
            else:
                print ("No file provided. Using default alphabet.")

        if option=="-o":
            if argument is not None:
                outname = argument
            else:
                outname = 'grid.txt'
                print ("No output filename provided. Using: "), (outname)

        if option=="-a":
            if argument is not None:
                alphabet = argument
            else:
                print ("No alphabet provided. Using default alphabet.")

    # Main program

    if inname:
        alphabet = alphabet_from_file(inname)

    grid = generate_grid(alphabet)
    i = 0

    print (alphabet)
    test_alphabet = [ch for ch in alphabet]
    last_char = test_alphabet.pop()
    test_alphabet.insert(0, last_char)
    last_char = test_alphabet.pop()
    test_alphabet.insert(0, last_char)
    test_alphabet = ''.join(test_alphabet)
    print (test_alphabet)
    print ('contains newline:'),(alphabet.count(r'\n'))
    try:
        for row in grid:
            line = ''.join(row)
            print (line)
    except UnicodeEncodeError:
        print ("Your console does not support unicode characters.")
        if outname:
            print ("Saving grid to file: "),(outname)
        else:
            print ("You can generate a grid to a file using '-o <filename>' option.")

    if outname:
        save_to_file(grid, outname)

if __name__ == "__main__":
   main(sys.argv[1:])



