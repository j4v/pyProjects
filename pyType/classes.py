#!/usr/bin/python2.7

class template:
	def __init__(self, inA, inB): # constructor => __ not _
		self.a = inA
		self.b = inB
	def add(self):
		return self.a + self.b
	def sub(self):
		return self.a - self.b

newC = Calculator(3,2)


# inheritance

class sciCalc(Calculator):
	def power(self):
		return pow(self.a, self.b)
