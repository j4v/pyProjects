#!/usr/bin/python2.7

# Author 				:	Xavier Garceau-Aranda
# Date 					:	7-10-2013
# Title 				:	httpGET.py
# Description				:	http GET on a giver page

#####################
# Imports           #
#####################

import sys

import scapy
from scapy.all import *

#####################
# Main	            #
#####################

# start with three-way handshake
# syn packet
syn = IP(dst='google.com') / TCP(dport=80, flags='S')
# receive syn-ack
syn_ack = sr1(syn)

#syn_ack.show()

# set TCP sequence and ack numbers
getStr = 'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'
request = IP(dst='google.com') \
          / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, \
                ack=syn_ack[TCP].seq + 1, flags='A') \
          / getStr
# send GET
reply = sr1(request)
# print reply
reply.show()




#request = IP(dst='stbl.polyhack.org') / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
