#!/usr/bin/python

# Author 				:	Xavier Garceau-Aranda
# Date 					:	26-07-2013
# Last modification 	:
# Title 				:	proxylister_v4.py
# Description			:	Parses ip:port from http://hidemyass.com, tests to 
#							see if the proxy is valid and writes results to a csv

# check : http://stackoverflow.com/questions/10860983/python-proxy-list-check

#####################
# Imports			#
#####################

import os
import string

import socket
import urllib
import urllib2

import threading
from multiprocessing import Process

from bs4 import BeautifulSoup
import premailer


#####################
# Variables			#
#####################

# all modules use socket so this sets the timeout for every request
socket.setdefaulttimeout(5)

base_url ="http://hidemyass.com/proxy-list/"


#####################
# Functions			#
#####################

# Determine if the ip and port is a valid http proxy
def valid_http(ip, port) :
	try :
		proxy_handler = urllib2.ProxyHandler({'http': 'http://'+ip+':'+port+'/'})
		proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
		opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
		opener.addheaders = [('User-agent','Mozilla/5.0')]
		opener.open('http://google.com')
	except Exception, e :
		#print e,' : ',self.proxy_type,self.ip
		return False
	else :
		return True

# Determine if the ip and port is a valid https proxy
def valid_https(ip, port) :
	try :
		proxy_handler = urllib2.ProxyHandler({'http': 'https://'+ip+':'+port+'/'})
		proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
		opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
		opener.addheaders = [('User-agent','Mozilla/5.0')]
		opener.open('http://google.com')
	except Exception, e :
		#print e,' : ',self.proxy_type,self.ip
		return False
	else :
		return True

# Try connecting to socks proxy
# Does not validate it as a proxy, just means it is up
def valid_socks(ip, port) :
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.ip,int(self.port)))
	except Exception, e :
		#print e,' : ',self.proxy_type,self.ip
		return False
	else :
		return True

# Parse the link page content and return ip
def parse_ip(link) :
	# get  content that could contain ip
	link_parse = str(link('span')[1]).split('<')

	# parse ip
	ip = ''
	i = 0
	for span in link_parse :
		if not 'style="display:none"' in span :
			try :
				octet = span.split('>')[1]
				octet = octet.strip('.')
				if octet.isdigit() :
					ip +=str(octet)+'.'
					i+=1
			except :
				pass
	# remove extra dot
	ip = ip[:-1]

	# unable to correctly parse some ips (2-7/page), so will skip them
	if i != 4 :
		return
	else :
		return ip

# Parse the link page content and return port
def parse_port(link) :
	return str(link('td')[2].string).split('\n')[1]

# Parse the link page content and return country
def parse_country(link) :
	return str(link('span')).split('.png"/> ')[1][:-8]

# Parse the link page content and return proxy type
def parse_proxy(link) :
	return string.lower(link('td')[-2].string).encode('ascii', 'ignore')

# Parse the link page content and return anonymity level
def parse_anonymity(link) :
	return link('td')[-1].string


#####################
# Classes			#
#####################

# Thread class that checks for a single ip if it is valid and if so 
# writes its infos in a file
class ip_thread(threading.Thread) : # subclass of threading.Thread

	def __init__(self, ip, port, country, proxy_type, anonymity_level, page) : 
		threading.Thread.__init__(self) # calls parent
		self.ip = ip
		self.port = port
		self.country = country
		self.proxy_type = proxy_type
		self.anonymity_level = anonymity_level
		self.page = page

	# essential method representing the thread's activity
	def run(self) :

		if 'http' == self.proxy_type :
			if valid_http(self.ip, self.port) :
				page_file = open(self.page, 'a')
				page_file.write(self.proxy_type+','+self.ip+','+self.port+','+self.country+','+self.anonymity_level+'\n')
				page_file.close()

		elif 'https' == self.proxy_type :
			if valid_https(self.ip, self.port) :
				page_file = open(self.page, 'a')
				page_file.write(self.proxy_type+','+self.ip+','+self.port+','+self.country+','+self.anonymity_level+'\n')
				page_file.close()

		elif 'socks' in self.proxy_type :
			if valid_socks(self.ip, self.port) :
				page_file = open(self.page, 'a')
				page_file.write(self.proxy_type+','+self.ip+','+self.port+','+self.country+','+self.anonymity_level+'\n')
				page_file.close()

# Process class that takes a webpage, finds the ips and dispatches threads to test them
class page_process(Process) :

	def __init__(self, url, page) : 
		Process.__init__(self)
		self.url = url
		self.page = page

	# essential method representing the process's activity
	def run(self) :

		print 'Process : ',self.page

		# create file for later use
		page_file = open(self.page, 'w')
		page_file.close()

		html = urllib.urlopen(self.url)
		# parse css to minimize attributes
		parsed_html = premailer.transform(html.read())
		bs = BeautifulSoup(parsed_html, "lxml")

		# get table containing infos
		linkTable = bs.find('table', {'id':'listtable', 'cellspacing':'0', 'cellpadding':'0', 'rel':'50'})

		# get table content
		linkList = linkTable('tr', {'class':''})
		linkList += linkTable('tr', {'class':'altshade'})
		# remove table headers
		linkList = linkList[1:51]

		# parse every link on the page
		link_job = [] # tread list
		for link in linkList :

			ip = parse_ip(link)

			# unable to correctly parse some ips (2-7/page), so will skip them
			if not ip :
				pass
			else :
				# parse all info
				port = parse_port(link)
				country = parse_country(link)
				proxy_type = parse_proxy(link)
				anonymity_level = parse_anonymity(link)

				# test ip with thread
				ipThread_worker = ip_thread(ip, port, country, proxy_type, anonymity_level, self.page)
				ipThread_worker.setDaemon(True)
				link_job.append(ipThread_worker)
				ipThread_worker.start()
		# start all threads
		for job in link_job :
			job.join()


#####################
# Main				#
#####################
def main() :

	jobs = []
	for page in range(1,17) :

		url = base_url + str(page)

		# start one process per page
		pageProcess_worker = page_process(url, str(page))
		pageProcess_worker.daemon = True
		jobs.append(pageProcess_worker)
		pageProcess_worker.start()

		for worker in jobs :
			worker.join()

	# make global file and remove temporary
	final_file = open('iplist_v4.csv', 'w')
	for page in range(1,17) :
		page_file = open(str(page), 'r').readlines()
		for line in page_file :
			final_file.write(line)
		os.remove(str(page))
	final_file.close()


#####################
# Run main			#
#####################

if __name__ == "__main__":
	main()

