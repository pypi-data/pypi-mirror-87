#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.v1.classes.config import *
import platform 

class Defaults(object):
	def __init__(self):

		# variables.
		self.os = platform.system().lower()
		if self.os in ["darwin"]: self.os = "osx"
		self.home = "/home/"
		self.media = "/media/"
		self.group = "root"
		self.user = os.environ.get("USER")
		if self.os in ["osx"]:
			self.home = "/Users/"
			self.media = "/Volumes/"
			self.group = "staff"

		#
	def check_operating_system(self, supported=["osx", "linux"]):
		if self.os in ["osx"] and self.os in supported: return "osx"
		elif self.os in ["linux"] and self.os in supported: return "linux"
		else: raise ValueError(f"Unsupported operating system: [{self.os}].")
	def check_alias(self, 
		# the source name.
		alias=None, 
		# the source path.
		executable=None,
	):
		path = f"/usr/local/bin/{alias}"
		if not os.path.exists(path) or '--create-alias' in sys.argv:
			file = f"""package={executable}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
			os.system(f"sudo touch {path}")
			os.system(f"sudo chmod 755 {path}")
			os.system(f"sudo chown {self.user}:{self.group} {path}")
			Files.File(path=f"{path}", data=file).save()
			os.system(f"sudo chmod 755 {path}")
			if '--silent' not in sys.argv:
				print(f'Successfully created alias: {alias}.')
				print(f"Check out the docs for more info $: {alias} -h")
		if '--create-alias' in sys.argv:
			quit()
	def get_source_path(self, path, back=1):
		return Formats.FilePath(path).base(back=back)

# initialized classes.
defaults = Defaults()