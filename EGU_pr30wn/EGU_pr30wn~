#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

import mechanize
import cookielib
from bs4 import BeautifulSoup

#import EGU_pr30wn_backend

# # # # variables



# # # # QT GUI

class Window(QtGui.QWidget):
    
	def __init__(self): # constructor
		super(Window, self).__init__() # returns the parent object of Window class
        	self.initUI()
        
	def initUI(self):
        
		# prerequisite buttons
		self.bouton1 = QtGui.QPushButton('Complete Prerequisite 1', self)
		self.bouton1.move(30, 60) 
		self.bouton1.clicked.connect(self.do1)

		self.bouton2 = QtGui.QPushButton('Complete Prerequisite 2', self)
		self.bouton2.move(30, 90) 
		self.bouton2.clicked.connect(self.do2)

		self.bouton3 = QtGui.QPushButton('Complete Prerequisite 3', self)
		self.bouton3.move(30, 120) 
		self.bouton3.clicked.connect(self.do3)

		# username input
		self.username = ''
		username = QtGui.QPushButton('Username', self)
		username.move(30, 20)
		username.clicked.connect(self.getUsername)

		# password input
		self.password = ''
		password = QtGui.QPushButton('Password', self)
		password.move(125, 20)
		password.clicked.connect(self.getPassword)

		# generate window
		self.setGeometry(300, 300, 240, 180)
		self.setWindowTitle('EGU pr30wn')
		self.setWindowIcon(QtGui.QIcon('hacker_icon.jpeg'))        
    		self.show()
        
	def getUsername(self):        
		text, ok = QtGui.QInputDialog.getText(self,'Username','Enter your username:') 
		if ok:
			self.username = text

	def getPassword(self):
		text, ok = QtGui.QInputDialog.getText(self,'Username','Enter your username:') 
		if ok:
			self.password = text

	def do1(self):
		print 'Clicked 1'
		print self.username
		print self.password
	def do2(self):
		print 'Clicked 2'
	def do3(self):
		print 'Clicked 3'






def main():
    
	app = QtGui.QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_()) # mainloop event handling


if __name__ == '__main__':
	main()   
