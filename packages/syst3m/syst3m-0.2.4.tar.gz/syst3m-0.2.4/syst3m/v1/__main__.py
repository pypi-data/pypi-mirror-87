#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, pathlib

## settings.
def __get_source_path__(package_name, index=1):
	executive_dir = str(pathlib.Path(__file__).absolute()).replace(os.path.basename(pathlib.Path(__file__)), '').replace("//","/")
	if executive_dir[len(executive_dir)-1] == "/": executive_dir = executive_dir[:-1]
	source, c = "/", 1
	for id in executive_dir.split("/"):
		if id == package_name:
			if c == index:
				source += id+"/"
				break
			else: c += 1
		else: source += id+"/"
	base = source[:-1].split("/")
	base = source.replace(f'/{base[len(base)-1]}/', '/')
	return source, base
SOURCE_NAME = "syst3m"
VERSION = "v1"
SOURCE_PATH, BASE = __get_source_path__(SOURCE_NAME)
sys.path.insert(1, BASE)

# imports.
from syst3m.v1.classes.config import *
from syst3m.v1.classes import utils, manager

# the cli object class.
class CLI(object):
	def __init__(self, alias=None):
		
		# variables.
		self.modes={
			"-h / --help":"Show the documentation.",
		},
		self.options={
		}
		self.alias = ALIAS
		self.documentation = self.__create_docs__()

		#
	def start(self):
		
		# help.
		if self.__argument_present__('-h') or self.__argument_present__('--help'):
			print(self.documentation)

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	# system functions.
	def __create_docs__(self):
		m = str(json.dumps(self.modes, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		#o = str(json.dumps(self.options, indent=4)).replace('    }','').replace('    {','').replace('    "','')[:-1][1:].replace('    "', "    ").replace('",',"").replace('": "'," : ")[2:][:-3]
		o = str(json.dumps(self.options, indent=4)).replace('{\n','').replace('}\n','').replace('    "','    ').replace('": "',' : ').replace('",\n','\n').replace('"\n','\n')[:-2]
		c = "\nAuthor: Daan van den Bergh \nCopyright: © Daan van den Bergh 2020. All rights reserved."
		doc = "Usage: "+self.alias+" <mode> <options> \nModes:\n"+m
		if o != "": doc += "\nOptions:\n"+o
		doc += c
		return doc
	def __argument_present__(self, argument):
		if argument in sys.argv: return True
		else: return False
	def __get_argument__(self, argument, required=True, index=1, empty=None):

		# check presence.
		if argument not in sys.argv:
			if required:
				raise ValueError(f"Define parameter [{argument}].")
			else: return empty

		# retrieve.
		y = 0
		for x in sys.argv:
			try:
				if x == argument: return sys.argv[y+index]
			except IndexError:
				if required:
					raise ValueError(f"Define parameter [{argument}].")
				else: return empty
			y += 1

		# should not happen.
		return empty
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
