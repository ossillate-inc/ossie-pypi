#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import generators

import os
import socket

from .command_base import CommandBase
import subprocess

class CheckDeps(CommandBase):
	def __init__(self, path, auth, creds, env):
		if not os.path.exists(path):
			print("%s does not exist. Exiting." % (path))
			exit(1)
		if not os.path.isfile(path):
			print("%s is not a valid Python deps file. Exiting." % (path))
			exit(1)
		path = os.path.expanduser(path)
		path = os.path.abspath(path)
		self.deps_filepath = path
		print("[+] Auditing deps @ ", self.deps_filepath)
		name = os.path.basename(self.deps_filepath)
		super().__init__("deps", name, auth, creds, env)

	def get_packages(self):
		try:
			print("    [+] Parsing %s for packages" % (self.deps_filepath))
			packages = self.get_packages_from_file(self.deps_filepath)
			if not packages or not len(packages):
				raise Exception("invalid deps file!")
			return packages
		except:
			print("Failed to audit. Exiting.")
			exit(1)
