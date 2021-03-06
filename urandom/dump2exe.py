#!/usr/bin/python2.7

# Author                :   j4v
# Date                  :   03-11-2013
# Title                 :   dump2exe.py
# Description           :
# Takes a hexdump (like one generated by xxd) and turns it back into 
# a binary executable
# Usage                 :   dump2exe.py in.dump out.exe

import sys

dumpFile = str(sys.argv[1])
exeFile = str(sys.argv[2])

dump = open(dumpFile, "r").readlines()

binaryString = ""
for i in dump :
    binaryString = binaryString+i.strip()

base = 0
outputString = ""
for i in binaryString :
    base += 1
    if (base%2 == 0) : # to use one out of two bytes and make pairs
        hexvalue += i
        letter = chr(int(hexvalue,16)) # to char
        outputString = outputString + letter
    else : # first byte of each pair
        hexvalue = i

out = open(exeFile, "w")
out.write(outputString)
out.close()
