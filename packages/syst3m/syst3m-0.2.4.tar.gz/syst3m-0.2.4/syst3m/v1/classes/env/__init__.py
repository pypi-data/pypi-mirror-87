#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.v1.classes.config import *

class Env(object):
	def __init__(self):
		a=1
		#
	def get_string(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else:
			return e
	def get_boolean(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		elif e in [True, "True", "true", "TRUE"]:
			return True
		else: 
			return False
	def get_integer(self, id, default=None):
		e = os.environ.get(id)
		try:
			return int(e)
		except:
			return default
	def get_array(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else: 
			a = []
			for i in e.split(","):
				a.append(self.__remove_whitespace__(i))
			return a
	def get_tuple(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else: 
			a = []
			for i in e.split(","):
				a.append(self.__remove_whitespace__(i))
			return tuple(a)
	def get_dictionary(self, id, default=None):
		e = os.environ.get(id)
		if e == None: 
			return default
		else: 
			a = []
			for i in e.split(","):
				a.append(self.__remove_whitespace__(i))
			d = {}
			for i in a:
				try:
					key,value = i.split(":")
					d[self.__remove_whitespace__(key)] = self.__remove_whitespace__(value)
				except: a=1
			return tuple(a)
	def __remove_whitespace__(self, string):
		if isinstance(string, str):
			for attempts in range(101):
				if string[0] == " ":
					string = string[1:]
				elif string[len(string)-1] == " ":
					string = string[:-1]
				else: break
		return string
	

# initialized classes.
env = Env()