#!/usr/bin/python

import os
import pprint
import sys
import mechanize
import cookielib
from bs4 import BeautifulSoup
import time
from optparse import OptionParser


# # # # manage user input

usageString = "Usage: %prog [options]"
parser = OptionParser(usage=usageString)
parser.add_option("-u", "--user", dest="username", metavar="USERNAMWE", type="string", 
	help="Username of the account to connect with")
parser.add_option("-p", "--password", dest="password", metavar="PASSWORD", type="string", 
	help="Password of the account to connect with")
parser.add_option("-m", "--max", dest="max_bid", metavar="MAXBID", type="int", 
	help="Maximum bid for the auction")
parser.add_option("-l", "--link", dest="bid_url", metavar="BIDURL", type="string", 
	help="URL of the auction page")

(opts,args) = parser.parse_args()

# more input than expected
if len(args) > 0:
	parser.error("Invalid additional option(s)")


# # # # variables

username = opts.username
password = opts.password
max_bid = opts.max_bid
bid_url = opts.bid_url

# check that has all necessary values
if not username and not password and not max_bid and not bid_url :
	parser.error("Missing options")
if not username :
	parser.error("Missing username")
if not password :
	parser.error("Missing password")
if not max_bid :
	parser.error("Missing maximum bid")
if not bid_url :
	parser.error("Missing auction URL")

good_response = '<Browser visiting https://signin.ebay.ca/ws/eBayISAPI.dll?co_partnerId=2&siteid=2&UsingSSL=1>'

bad_response = '<Browser visiting https://signin.ebay.ca/ws/eBayISAPI.dll?SignIn&errmsg=8&pUserId=xgarceauaranda&co_partnerId=2&siteid=2&pageType=-1&pa1=&i1=-1&UsingSSL=1&k=1&favoritenav=&bshowgif=0>'

url = 'https://signin.ebay.ca/ws/eBayISAPI.dll?SignIn'


# # # # create browser object

browser = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)

# Browser options (or else website sometimes throws 403 error)
browser.set_handle_equiv(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


# # # # functions

# print remaining time for the current bid
def get_remaining_time(page) :
	script_list =  page.find_all('script', type="text/javascript")
	for item in script_list:
		for line in item:
			if 'timeLeft' in line:

				if line[line.index(',"hoursLeft')-2] == ':' : # < 10 days 
					daysLeft = line[line.index("daysLeft")+10]
				else :
					daysLeft = line[line.index("daysLeft")+10:line.index("daysLeft")+12]

				if line[line.index(',"minutesLeft')-2] == ':' : # < 10 hours 
					hoursLeft = line[line.index("hoursLeft")+11]
				else :
					hoursLeft = line[line.index("hoursLeft")+11:line.index("hoursLeft")+13]

				if line[line.index(',"secondsLeft')-2] == ':' : # < 10 minutes 
					minutesLeft = line[line.index("minutesLeft")+13]
				else :
					minutesLeft = line[line.index("minutesLeft")+13:line.index("minutesLeft")+15]

				if line[line.index(',"siteId')-3] == ':' : # < 10 seconds 
					secondsLeft = line[line.index("secondsLeft")+13]
				else :
					secondsLeft = line[line.index("secondsLeft")+13:line.index("secondsLeft")+15]
				return [daysLeft, hoursLeft, minutesLeft, secondsLeft]
				break

# print the different options for the current bid
def print_options(page) :

	all = page.find_all('span', itemprop='price')

	buy_it_now = page.find_all('span', id='prcIsum')

	if len(buy_it_now) == 1 :
		print 'Buy It Now \t %s' %buy_it_now[0].get_text()

	place_bid = bid = [item for item in all if item not in buy_it_now]

	if len(place_bid) != 0 : 
		print 'Place Bid \t %s' %place_bid[0].get_text() 

	make_offer = page.find_all('a', id="boBtn_btn")
	if make_offer :
		print 'Make offer\t\t[x]'

# return the current price of the item
def get_current_price(page) :
	all = page.find_all('span', itemprop='price')
	buy_it_now = page.find_all('span', id='prcIsum')

	place_bid = bid = [item for item in all if item not in buy_it_now]

	price = place_bid[0].get_text().split('$')[1]
	return float(price)

# return the minimum possible bid for the auction
def get_min_bid(page) :
	text =  page.find_all('div', { "class" : "notranslate u-flL bid-note" })
	min_bid = text[0].get_text()[10:15].strip()
	if min_bid == 'than' : # error 
		min_bid = text[0].get_text()[20:26].strip()
	return min_bid

# takes time and converts to seconds
def get_seconds(day,hour,minute,second) :
	return int(int(day)*24*60*60+int(hour)*60*60+int(minute)*60+int(second))


# # # # main

# hide credentials
os.system('clear')
# header
print '\t\t Ebay AutoBidder \n'

print 'Visiting login page.'
browser.open(url)

# select the form to fill out for login
print 'Filling form ...',
browser.select_form(nr=1) 
browser.form['userid'] = username
browser.form['pass'] = password
browser.submit()

# check login success
if str(browser) == good_response :
	print 'Logged in. \n'
elif str(browser) == bad_response :
	sys.exit("Bad credentials \n")
else :
	sys.exit("Error \n")

# go to bid page
source = browser.open(bid_url)

# parse dada
html = source.read()
page = BeautifulSoup(html, 'lxml')

# get item title
title = page.find('title').text[1:len(page.find('title').text)-7] 

# print informations
print title
print '---------------------------'
remaining_time = get_remaining_time(page)	
print remaining_time[0]+'d '+remaining_time[1]+'h '+remaining_time[2]+'m '+remaining_time[3]+'s'
print '---------------------------'
print_options(page) 
print '---------------------------'
min_bid = get_min_bid(page)
print 'Min Bid \t %s \n' %min_bid

if (float(min_bid) > max_bid) :
	parser.error("You are bidding less than the minimum bid amount")

# wait till one minute before bid is over
seconds_remaining = get_seconds(remaining_time[0],remaining_time[1],remaining_time[2],remaining_time[3])
print 'Waiting till 30 seconds before end ... '
time.sleep(seconds_remaining-30)
print 'Start bidding ... \n'


bidded_amount = 0 # how much you have already bidded
while (float(min_bid) <= max_bid) and (seconds_remaining >= 0) :

	# go to bid page
	source = browser.open(bid_url)
	# parse dada
	html = source.read()
	page = BeautifulSoup(html, 'lxml')

	# check if auction still on
	remaining_time = get_remaining_time(page)	
	seconds_remaining = get_seconds(remaining_time[0],remaining_time[1],remaining_time[2],remaining_time[3])

	# check new min bid
	min_bid = get_min_bid(page)

	# bid if the last bid wasn't your's
	if bidded_amount != get_current_price(page) : 
		# place minimum bid
		print 'Bidding ...',
		#browser.select_form(nr=1) 
		#browser.form['maxbid'] = str(min_bid)
		#a = browser.submit()
		print 'done.'

		''' was this necessary?
		# confirm bid
		print 'Bidding confirmation ...',
		browser.select_form(nr=0) 
		#browser.form['maxbid'] = str(min_bid)
		browser.submit()
		print 'done.'
		'''

		print 'You bidded : '+min_bid
		bidded_amount = float(min_bid)
		

if (float(min_bid) > max_bid) :
	parser.error("You have been outbidded")
