#!/usr/bin/python2.7

# Author                :   j4v
# Date                  :   22-10-2013
# Title                 :   bitshift.py
# Description           :   bitshift like in C using ctypes

from ctypes import * # http://docs.python.org/2/library/ctypes.html

# lets say I want to work with a byte of value 0x1
print 'Normal types'
print (0b00000001 << 0) == 0b00000001
print (0b00000001 << 1) == 0b00000010
print (0b00000001 << 7) == 0b10000000
print (0b00000001 << 8) == 0b00000000

# now if we use ctypes and an unsigned byte
print '\nctypes'
print c_ubyte(0b00000001 << 0).value == 0b00000001
print c_ubyte(0b00000001 << 1).value == 0b00000010
print c_ubyte(0b00000001 << 7).value == 0b10000000
print c_ubyte(0b00000001 << 8).value == 0b00000000
