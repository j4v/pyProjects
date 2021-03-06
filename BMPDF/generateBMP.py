#!/usr/bin/python2.7

__author__      = "j4v"
__copyright__   = "Copyright 2013"
__license__     = "GPL v3"

# generateBMP.py
# Generates a simple bitmap file.
# Usage : ./generateBMP.py

#################
# IMPORTS       #
#################

import os
import sys
import struct

#################
# ARGUMENTS     #
#################

#################
# FUNCTIONS     #
#################

#################
# MAIN          #
#################

# Construct the bitmap header (yay INF1600)

#   should contain this :

#   424D 
#   xxxx xxxx     // size of header+content (bytes)
#   0000
#   0000
#   3600 0000
#   2800 0000
#   wwww wwww     // width (pixels)
#   hhhh hhhh     // height (pixels)
#   0100 
#   1800 
#   0000 0000 
#   xxxx xxxx     // size of content (bytes)
#   120B 0000 
#   120B 0000 
#   0000 0000 
#   0000 0000
#   [.. RBG ..]

staticHeader1 = chr(0x42)+chr(0x4D)
staticHeader2 = 4*chr(0x00)+chr(0x36)+3*chr(0x00)+chr(0x28)+3*chr(0x00)
staticHeader3 = chr(0x01)+chr(0x00)+chr(0x18)+5*chr(0x00)
staticHeader4 = 2*(chr(0x12)+chr(0x0B)+2*chr(0x00))+8*chr(0x00)

# WIDTH MUST BE A MULTIPLE OF 4

width = struct.pack('i', 4)
height = struct.pack('i', 4)
contentSize = struct.pack('i', 48)
totalSize = struct.pack('i', 54+48) 

# Construct the final bitmap header
bitmapHeader =  staticHeader1 + \
                totalSize + \
                staticHeader2 + \
                width + \
                height + \
                staticHeader3 + \
                contentSize + \
                staticHeader4

black = 3*chr(0x00)
white = 3*chr(0xff)

# make bitmap file content
bitmap = bitmapHeader + black + black + black + black + black + black + black + black + black + black + black + black + black + black + black + black
# write content to bitmap
out = open("test.bmp", "w")
out.write(bitmap)
out.close()
