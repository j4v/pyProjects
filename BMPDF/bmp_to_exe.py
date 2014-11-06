#!/usr/bin/python2.7

__author__      = "j4v"
__copyright__   = "Copyright 2013"
__license__     = "GPL v3"

# bmp_to_exe.py
# Works on a exe that was xored and stored into a bitmap
# Removes the header + padding, finds the value of the xor, unxors the file
# and saves it back to a exe.
# Usage : ./bmp_to_exe.py in.bmp out.exe

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

inBMP = sys.argv[1] # file to convert
outEXE = sys.argv[2] # file to output 

#################
# MAIN          #
#################

# Get bitmap content

BMP = open(inBMP, "r").readlines()
xoredEXE = "" # will contain all EXE's xored content

for line in BMP :

    line = line.strip() # remove that damn \n
    xoredEXE += line

# Remove header

xoredEXE = xoredEXE[54:]

# Remove padding

offset = 0
paddingLetter = xoredEXE[offset]

while(xoredEXE[offset] == paddingLetter) :
    offset += 1

xoredEXE = xoredEXE[offset:]

# Find the value of the XOR

xor = 0
while(chr(ord(xoredEXE[0])^xor) != 'M') :
    xor += 1

# unXOR the file

unxoredEXE = ""

for letter in xoredEXE :
    unxoredEXE += chr(ord(letter)^xor)

# Write content to exe

out = open(outEXE, "w")
out.write(unxoredEXE)
out.close()
