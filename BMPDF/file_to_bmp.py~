#!/usr/bin/python2.7

__author__      = "j4v"
__copyright__   = "Copyright 2013"
__license__     = "GPL v3"

# exe_to_bmp.py
# Takes a file, and generates a bmp for a given width.
# Usage : ./file_to_bmp.py in.file width out.file

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

inFile = sys.argv[1] # file to convert
width = int(sys.argv[2]
outBMP = sys.argv[3] # file to output 

#################
# FUNCTIONS     #
#################

# Takes value and returns the nearest greater square root
def nextGreaterSquareRoot(value) :

    # closest square to value
    squareRoot = int(math.floor(math.sqrt(value))+1)
    
    # if closest square is smaller then value, then next square is higher
    if squareRoot < value :
        # return next square
        return squareRoot + 1
    else :
        return squareRoot

# Takes a value and returns the nearest greater number divisible by 3
def nextDivisibleByThree(value) :
    while(value%3 != 0) :
        value += 1
    return value

#################
# MAIN          #
#################

#------------------------------------------------------------------------------#

# Take the exe and dump it into hex.dump file

os.system("xxd -ps "+inFile+" > hex.dump")

#------------------------------------------------------------------------------#

# Take the hex.dump and xor^0x13
# Someone could figure out the value of the XOR if they know it is a exe 
# by looking for the MX header.

EXE = open("hex.dump", "r").readlines()
xoredEXE = "" # will contain all EXE's xored content

for line in EXE :

    line = line.strip() # remove that damn \n

    for offset in range(0, len(line), 2) :

        decVal = int(line[offset] + line[offset+1], 16) # join 2 num/letter to make 
                                                        # hex value, store it as decimal
        xoredDecVal = decVal ^ xorValue # XOR the decimal
        xoredCharVal = chr(xoredDecVal) # convert back to ASCII char
        xoredEXE = xoredEXE + xoredCharVal # add to string

#------------------------------------------------------------------------------#

# Construct the bitmap header (yay INF1600)

#   should contain this :

#   42 4D 
#   xx xx xx xx     // size of header+content (bytes)
#   00 00
#   00 00
#   36 00 00 00
#   28 00 00 00
#   ww ww ww ww     // width (pixels)
#   hh hh hh hh     // height (pixels)
#   01 00 
#   18 00 
#   00 00 00 00 
#   xx xx xx xx     // size of content (bytes)
#   12 0B 00 00 
#   12 0B 00 00 
#   00 00 00 00 
#   00 00 00 00
#   [.. RBG ..]

#   will look like this :

#   hexdump        >  bitmap
#   h h h h h h h     p p e e 
#   p p e e e e e     e e e e 
#   e e e e           e e e e 

staticHeader1 = chr(0x42)+chr(0x4D)
staticHeader2 = 4*chr(0x00)+chr(0x36)+3*chr(0x00)+chr(0x28)+3*chr(0x00)
staticHeader3 = chr(0x01)+chr(0x00)+chr(0x18)+5*chr(0x00)
staticHeader4 = 2*(chr(0x12)+chr(0x0B)+2*chr(0x00))+8*chr(0x00)

headerLength = 54

# We want to generate an square image. 
# The first thing to take in account is that you need 3 bytes for one RBG pixel.
byteNumber = nextDivisibleByThree(len(xoredEXE))
pixelNumber = byteNumber / 3
# Then we calculate the nearest square root 
height = pixel/width
# Update values
pixelNumber = width*height
byteNumber = 3 * pixelNumber
# Calculate the padding
padding = ""

# Now we need to pack the sizes as little endian ASCII values
width = struct.pack('i', width)
height = struct.pack('i', height)
contentSize = struct.pack('i', byteNumber) 
totalSize = struct.pack('i', headerLength+byteNumber) 

# Construct the final bitmap header
bitmapHeader =  staticHeader1 + \
                totalSize + \
                staticHeader2 + \
                width + \
                height + \
                staticHeader3 + \
                contentSize + \
                staticHeader4

#------------------------------------------------------------------------------#

# Write bitmap header + padding + xored content to file.
# Cleanup temporary file

# make bitmap file content
bitmap = bitmapHeader + padding + xoredEXE
# write content to bitmap
out = open(outBMP, "w")
out.write(bitmap)
out.close()
# cleanup
os.system("rm hex.dump")
