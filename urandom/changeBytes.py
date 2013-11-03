#!/usr/bin/python2.7

# Author                :   j4v
# Date                  :   03-11-2013
# Title                 :   changeBytes.py
# Description           :
# Replaces octets from the IN hexdump for those in the OUT hexdump, starting
# at a predefined portion of th IN hexdump
# Usage                 :   changeBytes.py in.dump out.dump

import sys

dumpIN = str(sys.argv[1])
dumpOUT = str(sys.argv[2])


binary = open(dumpIN, "r").readlines()
pdf = open("noFLAGencoded.dump", "r").readlines()

binaryString = ""
for i in binary :
    binaryString = binaryString+i.strip()

pdfString = ""
for i in pdf :
    pdfString = pdfString+i.strip()

offset = binaryString.find("7d081c1e7569") # predefined portion of IN hexdump

output = binaryString[0:offset] + \
        pdfString + \
        binaryString[offset+len(pdfString):]

out = open(dumpOUT, "w")
out.write(output)
out.close()

