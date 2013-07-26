#!/usr/bin/python

import sys
import mechanize
import cookielib
from bs4 import BeautifulSoup

# # # # variables

username = str(sys.argv[1])
password = str(sys.argv[2])

good_response = '<Browser visiting http://www.enigmagroup.org/forums/index.php>'
bad_response = '<Browser visiting http://www.enigmagroup.org/forums/index.php?action=login2>'

url = 'http://www.enigmagroup.org/'

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

# # # #

def login() :
	
	browser.open(url)
	print str(browser) + '\n'
	
	# select the form to fill out
	print 'filling form ... \n'
	browser.select_form(nr=1) 
	browser.form['user'] = username
	browser.form['passwrd'] = password
	browser.submit()

	if str(browser) == good_response :
		print 'Logged in. \n'
	elif str(browser) == bad_response :
		print 'Bad credentials \n'
	else :
		print 'Error \n'

#------------------------------------------- Prerequisite 1

def complete_pre1() :

	source = browser.open('http://www.enigmagroup.org/missions/basics/pre/1')
	
	# find password in source
	html = source.read()
	bs = BeautifulSoup(html, 'lxml')
	password_pre1 = str(bs.getText)[1232:1238] # parse html to find fixed-length password

	# select the form to fill out
	print 'filling form ... \n'
	browser.select_form(nr=0) 
	browser.form['password'] = password_pre1
	response = browser.submit()
	
	print "Prerequesite 1 completed. \n"

#------------------------------------------- Prerequisite 2

def complete_pre2() :

	browser.open('http://www.enigmagroup.org/missions/basics/pre/2')

	# select the form to fill out
	print 'filling form ... \n'
	browser.select_form(nr=0) 
	browser.form['u'] = 'admin'
	browser.form['p'] = 'rosebud101z'
	response = browser.submit()	

	# check if correct answer
	html = response.read()
	bs = BeautifulSoup(html, 'lxml')

	print "Prerequesite 2 completed. \n"

#------------------------------------------- Prerequisite 3

def complete_pre3() :

	browser.open('http://www.enigmagroup.org/missions/basics/pre/3')

	# select the form to fill out
	print 'filling form ... \n'
	browser.select_form(nr=0) 
	browser.form['u'] = 'admin'
	browser.form['p'] = 'f0rkblork'
	response = browser.submit()

	# check if correct answer
	html = response.read()
	bs = BeautifulSoup(html, 'lxml')

	print "Prerequesite 3 completed. \n"


