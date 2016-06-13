#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
This program generates a N*N grid of securely random symbols.

Usage:
python run.py <options>

-i <filename>      Use alphabet from a file.
-o <filename>      Write output to a file.
-a "<alphabet>"    Enter custom alphabet using keyboard.
                   May not work properly with unicode characters - use -i and o- instead.
-r <count>         Generate multiple grids.
"""

import sys
import getopt
import codecs
import random
import os
import fcntl, termios, struct

# This line is needed to fix utf-8 in Wondows command line.
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

rand_generator = random.SystemRandom()
default_alphabet = (u"abcdefghijklmnopqrstuvwxyz"
                   u"èéêëēėęÿûüùúūîïíīįìôöòóœøōõàáâäæãåāßśšłžźżçćčñń")


def random_char(alph):
    """Returns a random char using a string as it's alphabet"""
    char = alph[rand_generator.randrange(len(alph))]
    return char


def random_num(alph):
    return rand_generator.randrange(len(alph))


def generate_line(alphabet):
    """Returns a string containing all characters from alphabet in random order."""
    array = [ch for ch in alphabet]
    line = []
    for i in range(len(alphabet)):
        line.append(array.pop(random_num(array)))

    return line


def mix_rows(grid):
    """Randomly chooses and exchanges 2 rows in the grid.

    Does not return a new grid, operates on the specified instead.
    """

    index1 = rand_generator.randrange(len(grid))
    index2 = rand_generator.randrange(len(grid))
    while index1 == index2:
        index2 = rand_generator.randrange(len(grid))

    grid[index1], grid[index2] = grid[index2], grid[index1]


def mix_cols(grid):
    """Randomly chooses and exchanges 2 columns in the grid.

    Does not return a new grid, operates on the specified instead.
    """

    index1 = rand_generator.randrange(len(grid))
    index2 = rand_generator.randrange(len(grid))
    while index1 == index2:
        index2 = rand_generator.randrange(len(grid))

    for row in grid:
        row[index1], row[index2] = row[index2], row[index1]


def mix_grid(grid):
    """Randomly mixes the rows and columns in the grid."""
    iterations = rand_generator.randrange(100*len(grid), 1000*len(grid))
    i = 0
    while i < iterations:
        row_or_column = rand_generator.randrange(2)

        if row_or_column == 1:
            mix_cols(grid)
        else:
            mix_rows(grid)

        i += 1


def generate_grid(alphabet):
    """Generates a unique grid using the specified alphabet."""
    random_line = generate_line(alphabet)
    array = random_line[:]
    grid = []
    for i in range(len(random_line)):
        new_array = array[:]
        grid.append(new_array)
        last_char = array.pop()
        array.insert(0, last_char)

    mix_grid(grid)

    return grid


def check_norepeat(grid):
    """Checks the 'no-repeat' requirement.

    Each symbol in the grid must be unique in it's row and columnt.'
    Returns False if the requirement is not fulfilled, Else returns true.
    """

    def conflict(gr, row, col):
        char = gr[row][col]
        r = gr[row]
        c = [row[col] for row in gr]

        rowcount = r.count(char)
        colcount = c.count(char)

        if (rowcount != 1) or (colcount != 1):
            return True

        return False

    norepeat = True

    for row in range(len(grid)):
        for col in range(len(grid)):
            if conflict(grid, row, col):
                norepeat = False

    return norepeat

def save_grids(grid_array, filepath):
    """Saves the multiple grids to a file specified by filepath."""
    outfile = codecs.open(filepath, mode='w+', encoding='utf-8')
    for grid in grid_array:
        outfile.writelines([((''.join(row)) + u'\n') for row in grid])
        # outfile.write(''.join(['-' for i in range(len(grid_array[0]))]))
        outfile.write('-'*(len(grid_array[0])))
        outfile.write(u'\n')



def alphabet_from_file(filepath):
    """Reads first line from the file specified by filepath and returns it without the trailing new line."""
    alph = codecs.open(filepath, encoding='utf-8').readline()
    # Remove newline
    alph = alph[:-1]
    return alph


def get_terminal_width(count=1):

    h, w, hp, wp = struct.unpack('HHHH',
                                 fcntl.ioctl(0, termios.TIOCGWINSZ,
                                             struct.pack('HHHH', 0, 0, 0, 0)))
    return w

def generate_multiple(alphabet, count):
    # ter_width = get_terminal_width()[0]
    #
    # grids_per_row = ter_width//(len(alphabet) + 1)
    grid_arr = [generate_grid(alphabet) for gr in range(count)]
    return grid_arr


def main(argv):
    inname = ''
    alphabet = default_alphabet
    outname = ''
    count = 1

    try:
        opts, args = getopt.getopt(argv, "i:o:r:a:h", ['help'])
    except getopt.GetoptError:
        # TODO: Print help for the user
        sys.exit(2)

    # Processing options
    for option, argument in opts:
        if option == "-i":
            if argument:
                inname = argument
            else:
                print ("No file provided. Using default alphabet.")

        if option == "-o":
            if argument:
                outname = argument
            else:
                outname = 'grid.txt'
                print ("No output filename provided. Using: "), (outname)

        if option == "-a":
            if argument:
                alphabet = argument.decode('utf-8')
            else:
                print ("No alphabet provided. Using default alphabet.")

        if option == "-h" or option == "--help":
            print (__doc__)
            return 0

        if option == "-r":
            if int(argument):
                count = int(argument)

    # Main program

    if inname:
        if os.path.isfile(inname):
            alphabet = alphabet_from_file(inname)
        else:
            print ("File does not exist. Using default alphabet.")

    alphabet = ''.join(set(alphabet))

    grid_arr = generate_multiple(alphabet, count)

    line_arr = [[] for i in range(len(alphabet))]
    allowed = get_terminal_width() // (len(alphabet) + 1)

    if allowed == 0:
        allowed = 1
    grids_per_row = 0

    try:
        for grid in grid_arr:

            for row_index in range(len(alphabet)):
                for char in grid[row_index]:
                    line_arr[row_index].append(char)
                line_arr[row_index].append('|')

            grids_per_row += 1

            if grids_per_row == allowed:
                for line in line_arr:
                    print (''.join(line))
                print ('-'*(len(alphabet)+1)*allowed)
                grids_per_row = 0
                line_arr = [[] for i in range(len(alphabet))]

        if line_arr:
            if line_arr[0]:
                for line in line_arr:
                    print (''.join(line))


    except UnicodeEncodeError:
        print ("Your console does not support unicode characters.")
        if outname:
            print ("Saving grid to file: "), (outname)
        else:
            print ("You can generate a grid to a file using '-o <filename>' option.")

    if outname:
        if os.path.isfile(outname):
            answer = ''
            while answer != 'y':
                answer = raw_input("File already exists. Overwrite? (y/n): ")
                if answer == 'y':
                    save_grids(grid_arr, outname)
                elif answer == 'n':
                    print ("Not saving to file.")
                    break
        else:
            save_grids(grid_arr, outname)

if __name__ == "__main__":
    main(sys.argv[1:])



