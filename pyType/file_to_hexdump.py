#!/usr/bin/python2.7

__author__      = "j4v"
__copyright__   = "Copyright 2013"
__license__     = "GPL v3"

# exe_to_bmp.py
# Takes a file, xor's every byte and stores the result in a bitmap file.
# Usage : ./exe_to_bmp.py in.exe 13 out.bmp

#################
# IMPORTS       #
#################

import os
import sys
import struct
import math

#################
# ARGUMENTS     #
#################

inFile = sys.argv[0] # input file
print inFile

#################
# FUNCTIONS     #
#################

# Def:      takes a file and returns the corresponding hexdump
# input :   file
# output :  hexdump
def fileToHexDump(file) :
    ASCIIdump = ''
    for line in file :
        ASCIIdump += line.strip()
    HEXdump = ''
    for letter in ASCIIdump :
        HEXdump += ord(letter)
    return HEXdump
    
#################
# MAIN          #
#################

file = open(inFile, "r").readlines()
hexDump = fileToHexDump(file)
print hexDump
file.close()
